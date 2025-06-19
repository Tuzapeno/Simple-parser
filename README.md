# Simple Formula Parser

This project showcases a basic parser for validating simple logical formulas. It's built to demonstrate fundamental concepts like tokenization and parsing using a finite state machine and recursive descent parsing.

## Usage

This project is a showcase and not intended for general use.

For demonstration purposes, it expects a single command-line argument: a path to a `.txt` file. The first line of this file must contain an integer indicating the number of logical expressions that follow, with each expression on a new line.

Grammar

The parser adheres to the following grammar rules:

    FORMULA = CONSTANTE | PROPOSICAO | FORMULAUNARIA | FORMULABINARIA
    CONSTANTE = true | false
    PROPOSICAO = [0-9][0-9a-z]*
    FORMULAUNARIA = ABREPAREN OPERADORUNARIO FORMULA FECHAPAREN
    FORMULABINARIA = ABREPAREN OPERATORBINARIO FORMULA FORMULA FECHAPAREN
    ABREPAREN = (
    FECHAPAREN = )
    OPERATORUNARIO = \neg
    OPERATORBINARIO = \wedge | \vee | \rightarrow | \leftrightarrow

