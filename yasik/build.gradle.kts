plugins {
    antlr
}

repositories {
    mavenCentral()
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(11))
    }
}

dependencies {
    val antlrVersion = file("pyproject.toml").readLines()
        .mapNotNull { Regex("""antlr4-python3-runtime\s*=\s*\".?(\d+\.\d+(\.\d+)?)"$""").matchEntire(it) }
        .first()
        .groupValues[1]
    antlr("org.antlr:antlr4:$antlrVersion")
}

tasks.generateGrammarSource.configure {
    arguments = listOf(
        "-Dlanguage=Python3",
        "${projectDir}/src/main/antlr/Yasik.g4",
//        "-o", "${projectDir}/src/main/python/yasik",
    )
    outputDirectory = file("${projectDir}/yasik/parser_generated")
}

