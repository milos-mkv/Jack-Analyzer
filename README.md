# Jack-Analyzer

Jack analyzer is simple program that produces xml code from provided jack files.

## Example
Simple jack program:
~~~~~~.jack
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/09/Square/Main.jack

/**
 * The Main class initializes a new Square Dance game and starts it.
 */
class Main {

    /** Initializes a new game and starts it. */    
    function void main() {
        do Output.print("Hello world!");
        return;
    }
}
~~~~~~
Jack analyzer output:
~~~~~~.xml
<class>
    <keyword> class </keyword>
    <identifier> Main </identifier>
    <symbol> { </symbol>
    <subroutineDec>
        <keyword> function </keyword>
        <keyword> void </keyword>
        <identifier> main </identifier>
        <symbol> ( </symbol>
        <parameterList>
        </parameterList>
        <symbol> ) </symbol>
        <subroutineBody>
            <symbol> { </symbol>
            <statements>
                <doStatement>
                    <keyword> do </keyword>
                    <subroutineCall>
                        <identifier> Output </identifier>
                        <symbol> . </symbol>
                        <identifier> print </identifier>
                        <symbol> ( </symbol>
                        <expressionList>
                            <expression>
                                <term>
                                    <stringConstant> Hello world! </stringConstant>
                                </term>
                            </expression>
                        </expressionList>
                        <symbol> ) </symbol>
                    </subroutineCall>
                    <symbol> ; </symbol>
                </doStatement>
                <returnStatement>
                    <keyword> return </keyword>
                    <symbol> ; </symbol>
                </returnStatement>
            </statements>
            <symbol> } </symbol>
        </subroutineBody>
    </subroutineDec>
    <symbol> } </symbol>
</class>
~~~~~~