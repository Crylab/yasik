#!/usr/bin/env python

import numpy as np
import time
from copy import copy
from subprocess import DEVNULL, STDOUT, check_call
import subprocess
import lib
from multiprocessing import Process

def do_in_parallel(n_cores, queue, global_data):

    queue_exe = queue["in"]
    queue_out = queue["out"]
    queue_exp = queue["exp"]

    procs = []
    exec_list = sorted(queue_exe)        

    while exec_list:
        cpu_available = n_cores
        for i in range(n_cores):
            command = "copy "+global_data["xml"]+".xml "+global_data["xml"]+str(i+1)+".xml"
            subprocess.call(command, shell=True)
        while exec_list and cpu_available>0:
            # chunk
            cpu_available -= 1
            key = exec_list.pop(0)        
            local_in_list = queue_exe[key]
            local_out_dict = queue_out[key]
            local_exp = queue_exp[key]
            local_data = {"in": local_in_list, "out": local_out_dict, "exp": local_exp}
            proc = Process(target=optimization, args=(cpu_available+1, local_data, global_data))
            procs.append(proc)
            proc.start()
        # complete the processes
        for proc in procs:
            proc.join()
        for i in range(n_cores):
            command = "del "+global_data["xml"]+str(i+1)+".xml"
            subprocess.call(command, shell=True)


def optimization(id, local_data, global_data):

        local_in_list = local_data["in"]
        local_out_dict = local_data["out"]
        local_exp = local_data["exp"]
        start_time = time.time()

        semi_simulated_laptimer = global_data["simulated_laptimer"]
        data_ref_trans_laptimer = global_data["data_ref_trans_laptimer"]
        exe = global_data["exe"]
        semi_xml = global_data["xml"]
        config = global_data["config"]
        out_list = global_data["out_list"]
        optim_type = config["config"]["optimization"]
        alias = config["output_aliasing"]
        mat = config["mat_outputs"]


        xml = semi_xml+str(id)+".xml"
        simulated_laptimer = semi_simulated_laptimer+str(id)+".txt"

        def simulation():
            # Run simulation
            cost = 0.0
            if local_exp == "top_speed":
                print("Run simulation")
                check_call(exe+" topspeed", stdout=DEVNULL, stderr=STDOUT)
                print("Simulation is over")
                # Fetch the data
                print("Data parsing")
                data = lib.PiTecParsing(simulated_top)
                data_trans = lib.dictTrans(data, alias, mat["top_speed"])
                print("Data processing")
                data_ref_trans = data_ref_trans_top
            elif local_exp == "snail":
                print("Run simulation")
                check_call(exe+" snail", stdout=DEVNULL, stderr=STDOUT)
                print("Simulation is over")
                # Fetch the data
                print("Data parsing")
                data = lib.PiTecParsing(simulated_snail)
                data_trans = lib.dictTrans(data, alias, mat["snail"])
                print("Data processing")
                data_ref_trans = data_ref_trans_snail
            elif local_exp == "laptimer":
                print("Run simulation")
                try:
                    check_call(exe+" laptimer "+str(id), stdout=DEVNULL, stderr=STDOUT)
                except subprocess.CalledProcessError as e:
                    print("Simulator was unable to complete the lap.")
                    return 999999.9
                print("Simulation is over")
                # Fetch the data
                print("Data parsing")
                data = lib.PiTecParsing(simulated_laptimer)
                data_trans = lib.dictTrans(data, alias, mat["laptimer"])
                print("Data processing")
                data_ref_trans = data_ref_trans_laptimer
            else:
                print("ERROR: unknown type of experiment")
            # Cost calc
            for each in local_out_dict:
                arg = local_out_dict[each]["wrt"]
                mult = local_out_dict[each]["multiplicator"]
                # Filtering
                if "filter" in local_out_dict[each] and local_out_dict[each]["filter"] is not None:
                    cond = local_out_dict[each]["filter"]
                    cond_list = []
                    for every in out_list:
                        if every in cond:
                            cond_list.append(every)
                data_list_sim = []
                for idx in range(len(data_trans[each])):
                    if "filter" in local_out_dict[each] and local_out_dict[each]["filter"]is not None:
                        cond = local_out_dict[each]["filter"]
                        for every in cond_list:
                            data = data_trans[every][idx]
                            cond2 = cond.replace(every, str(data))
                            cond = cond2
                        cond_is_ok = eval(cond)
                    else:
                        cond_is_ok = True
                    fun_val = data_trans[each][idx]
                    arg_val = data_trans[arg][idx]
                    if cond_is_ok:
                        data_list_sim.append((arg_val, fun_val))
                data_list_ref = []
                for idx in range(len(data_ref_trans[each])):
                    if "filter" in local_out_dict[each] and local_out_dict[each]["filter"]is not None:
                        cond = local_out_dict[each]["filter"]
                        for every in cond_list:
                            data = data_ref_trans[every][idx]
                            cond2 = cond.replace(every, str(data))
                            cond = cond2
                        cond_is_ok = eval(cond)
                    else:
                        cond_is_ok = True
                    fun_val = data_ref_trans[each][idx]
                    arg_val = data_ref_trans[arg][idx]
                    if cond_is_ok:
                        data_list_ref.append((arg_val, fun_val))
                if local_out_dict[each]["cost"] == "interp_square_cost":
                    cost += mult * lib.subtractSquareCostInterp(data_list_sim, data_list_ref)
                elif local_out_dict[each]["cost"] == "closest_square_cost":
                    cost += mult * lib.subtractSquareCost(data_list_sim, data_list_ref)
                elif local_out_dict[each]["cost"] == "regress_square_cost":
                    cost += mult * lib.subtractSquareCostRegres(data_list_sim, data_list_ref)
                elif local_out_dict[each]["cost"] == "lowpass_square_cost":
                    cost += mult * lib.subtractSquareCostLowPass(data_list_sim, data_list_ref)
                else: 
                    print("Error: Unknown type of cost function")
                    quit()
            print("Current cost is: "+str(cost))
            return cost

        def gradient_normalization(gradient):
            result = {}
            square_sum = 0.0
            for each in gradient:
                square_sum += gradient[each]**2
            for each in gradient:
                result[each] = gradient[each]/np.sqrt(square_sum)
            return result
    
        # Optimization
        if optim_type == "gradient_descent":
            base_cost = 0.0
            state = {}
            while(True):
                gradient = {}
                previous_cost = base_cost
                base_cost = simulation()
                print("Base cost is: "+str(base_cost))
                if previous_cost>0.0 and previous_cost<base_cost:
                    print("Founded values:")
                    print(state)
                    for input in local_in_list:
                        access_w = config["inputs"][input]["access_w"]
                        exec("value_script_update = "+str(state[input])+"; "+access_w)
                    break
                for input in local_in_list:
                    access_r = config["inputs"][input]["access_r"]
                    access_w = config["inputs"][input]["access_w"]
                    value = eval(access_r)
                    state[input] = value
                    tol = config["inputs"][input]["tolerance"]
                    exec("value_script_update = "+str(value+tol)+"; "+access_w)
                    local_cost = simulation()
                    exec("value_script_update = "+str(value)+"; "+access_w)
                    gradient[input] = (base_cost-local_cost)/tol
                norm_gradient = gradient_normalization(gradient)
                print("Gradient computed: "+str(norm_gradient))
                print("New set of values: ")
                for input in local_in_list:
                    value = state[input]
                    tol = config["inputs"][input]["tolerance"]
                    partial = norm_gradient[input]
                    new_value = value+(partial*tol)
                    val_max = config["inputs"][input]["init_val"]
                    val_min = config["inputs"][input]["init_step"]
                    if new_value>val_max or new_value<val_min:
                        new_value = value
                    print(input+": "+str(new_value))
                    access_w = config["inputs"][input]["access_w"]
                    exec("value_script_update = "+str(new_value)+"; "+access_w)
                    
        elif optim_type == "coordinate_descent":
            state = {}
            for input in local_in_list:
                access_r = config["inputs"][input]["access_r"]
                state[input] = eval(access_r)
            while(True): 
                updates = 0
                for input in local_in_list:
                    base_cost = simulation()
                    print("Base cost is: "+str(base_cost))
                    access_r = config["inputs"][input]["access_r"]
                    access_w = config["inputs"][input]["access_w"]
                    tol = config["inputs"][input]["tolerance"]
                    value = eval(access_r)
                    exec("value_script_update = "+str(value+tol)+"; "+access_w)
                    local_cost = simulation()
                    exec("value_script_update = "+str(value)+"; "+access_w)
                    direction = np.sign(base_cost-local_cost)
                    val_max = config["inputs"][input]["init_val"]
                    val_min = config["inputs"][input]["init_step"]
                    while(True):
                        new_value = value+(direction*tol)
                        if new_value>val_max or new_value<val_min:
                            print(input+": Reached limit")
                            break
                        exec("value_script_update = "+str(new_value)+"; "+access_w)
                        local_cost = simulation()
                        if local_cost>base_cost:
                            exec("value_script_update = "+str(value)+"; "+access_w)
                            print("Optimal value for "+input+": "+str(value))
                            break
                        base_cost = local_cost
                        value = new_value
                    if state[input]==value:
                        updates +=1
                    else:
                        state[input] = value
                if updates == len(local_in_list):
                    print("Optimum set founded")
                    print(state)
                    break

        elif optim_type == "nelder_mead":
            state = {}
            tolerance = {}
            print("Computing initial simplex of "+str(len(local_in_list)+1)+" points")
            for input in local_in_list:
                access_w = config["inputs"][input]["access_w"]
                init_val = config["inputs"][input]["init_val"]
                init_step = config["inputs"][input]["init_step"]
                exec("value_script_update = "+str(init_val)+"; "+access_w)
                #value = eval(access_r)
                state[input] = init_val
            prev_best = simulation()
            res = [[state, prev_best]]
            for input in local_in_list:
                state_updated = copy(state)
                access_r = config["inputs"][input]["access_r"]
                access_w = config["inputs"][input]["access_w"]
                init_val = config["inputs"][input]["init_val"]
                init_step = config["inputs"][input]["init_step"]
                #value = eval(access_r)
                tol = config["inputs"][input]["tolerance"]
                tolerance[input] = tol
                exec("value_script_update = "+str(init_val+init_step)+"; "+access_w)
                local_cost = simulation()
                exec("value_script_update = "+str(init_val)+"; "+access_w)
                state_updated[input] = init_val+init_step
                res.append([state_updated, local_cost])            
            print("Initial simplex was computed! ")            
            no_improv = 0
            iters = 0
            while(True):
                # order
                res.sort(key=lambda x: x[1])
                print("Brand new iteration:")
                print(res)
                best = res[0][1]
                dim = len(state)
                alpha=1.0
                if dim>2:
                    gamma=1+(2/dim)
                    rho=-(0.75-(1/(2*dim)))
                    sigma=1-(1/dim)
                else:
                    gamma=2
                    rho=-0.5
                    sigma=0.5
                no_improve_thr = 1e-3
                no_improv_break=100

                if best < prev_best - no_improve_thr:
                    no_improv = 0
                    prev_best = best
                else:
                    no_improv += 1

                if no_improv >= no_improv_break:
                    print("There is no improvement "+str(no_improv_break)+" times in a row. Best founded is:")
                    print(res[0])
                    break

                out_points = 0
                for input in local_in_list:
                    arr = []
                    for tup in res:
                        arr.append(tup[0][input])
                    max_val = max(arr)
                    min_val = min(arr)
                    width = (max_val-min_val)*2.0
                    if width<tolerance[input]:
                        out_points+=1
                if out_points>=len(local_in_list):
                    print("Tolerance reached! The best set is:")
                    print(res[0])
                    print("Execution time from the beginning: "+str((time.time()-start_time)/60.0)+" minutes")
                    xml = semi_xml+".xml"
                    for input in local_in_list:
                        access_w = config["inputs"][input]["access_w"]
                        exec("value_script_update = "+str(res[0][0][input])+"; "+access_w)
                    break
                if no_improv >= no_improv_break:
                    print("There is no improvement "+str(no_improv_break)+" times in a row. Best founded is:")
                    print(res[0])
                    break
        
                # centroid
                x0 = {}
                for key in state:
                    x0[key] = 0.0
                for tup in res[:-1]:
                    for key, value in tup[0].items():
                        x0[key] += value/(len(res)-1)
        

                # reflection
                xr = {}
                for key in state:
                    xr[key] = x0[key] + alpha*(x0[key] - res[-1][0][key])
                for input in local_in_list:
                    access_w = config["inputs"][input]["access_w"]
                    exec("value_script_update = "+str(xr[input])+"; "+access_w)
                rscore = simulation()
                for input in local_in_list:
                    access_w = config["inputs"][input]["access_w"]
                    exec("value_script_update = "+str(state[input])+"; "+access_w)
                if res[0][1] <= rscore < res[-2][1]:
                    print("reflect")
                    del res[-1]
                    res.append([xr, rscore])
                    continue

                # expansion
                if rscore < res[0][1]:
                    xe = {}
                    for key in state:
                        xe[key] = x0[key] + gamma*(x0[key] - res[-1][0][key])
                    for input in local_in_list:
                        access_w = config["inputs"][input]["access_w"]
                        exec("value_script_update = "+str(xe[input])+"; "+access_w)
                    escore = simulation()
                    for input in local_in_list:
                        access_w = config["inputs"][input]["access_w"]
                        exec("value_script_update = "+str(state[input])+"; "+access_w)
                    print("expansion")
                    if escore < rscore:
                        del res[-1]
                        res.append([xe, escore])
                        continue
                    else:
                        del res[-1]
                        res.append([xr, rscore])
                        continue

                if dim==1:
                    xc = {}
                    for key in state:
                        xc[key] = x0[key] + rho*(x0[key] - res[-1][0][key])
                    for input in local_in_list:
                        access_w = config["inputs"][input]["access_w"]
                        exec("value_script_update = "+str(xc[input])+"; "+access_w)
                    cscore = simulation()
                    for input in local_in_list:
                        access_w = config["inputs"][input]["access_w"]
                        exec("value_script_update = "+str(state[input])+"; "+access_w)                    
                    del res[-1]
                    res.append([xc, cscore])
                else:
                    # contraction
                    if rscore>=res[-2][1]:
                        xc = {}
                        for key in state:
                            xc[key] = x0[key] + rho*(x0[key] - res[-1][0][key])
                        for input in local_in_list:
                            access_w = config["inputs"][input]["access_w"]
                            exec("value_script_update = "+str(xc[input])+"; "+access_w)
                        cscore = simulation()
                        for input in local_in_list:
                            access_w = config["inputs"][input]["access_w"]
                            exec("value_script_update = "+str(state[input])+"; "+access_w)
                        if cscore < res[-2][1]:
                            print("contraction inside")
                            del res[-1]
                            res.append([xc, cscore])
                            continue
                    else:
                        xc = {}
                        for key in state:
                            xc[key] = x0[key] - rho*(x0[key] - res[-1][0][key])
                        for input in local_in_list:
                            access_w = config["inputs"][input]["access_w"]
                            exec("value_script_update = "+str(xc[input])+"; "+access_w)
                        cscore = simulation()
                        for input in local_in_list:
                            access_w = config["inputs"][input]["access_w"]
                            exec("value_script_update = "+str(state[input])+"; "+access_w)
                        if cscore < res[-2][1]:
                            print("contraction outside")
                            del res[-1]
                            res.append([xc, cscore])
                            continue


                    # reduction
                    x1 = res[0][0]
                    nres = [res[0]]
                    print("reduction")

                    for tup in res[1:]:
                        redx = {}
                        for key in state:
                            redx[key] = x1[key] + sigma*(tup[0][key] - x1[key])
                        for input in local_in_list:
                            access_w = config["inputs"][input]["access_w"]
                            exec("value_script_update = "+str(redx[input])+"; "+access_w)
                        score = simulation()
                        for input in local_in_list:
                            access_w = config["inputs"][input]["access_w"]
                            exec("value_script_update = "+str(state[input])+"; "+access_w)
                        nres.append([redx, score])
                    res = nres




