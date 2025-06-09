package analizadorsintactico;
import java.util.ArrayList;
import java_cup.runtime.*;
%%

%class Lexer
%line
%column 
%cup
%ignorecase

%{
    public String errlex="";
    public ArrayList<Token> ts = new ArrayList<Token>(); 
    public Symbol symbol(int type, Object value){
        return new Symbol(type,yyline,yycolumn, value);
    }
%}

a =       [a-zA-Z]
n =       [0-9]
espacio = [\n\t\r ]

numero        = {n}+("."{n}+)?
identificador = {a}({a}|{n}|"_")*

constante_alfanumerica = \"[^\"]*\"

operador_aritmetico = "+" | "-" | "*" |"/"
operador_relacional = "<" |"<="| ">="|"=="|"!="|">"
operador_logico     = "|"|"&"

asignacion = "="
punto_coma = ";"
dos_puntos = ":"
coma       = ","

parentesis_izquiedo = "("
parentesis_derecho  = ")"

//Palabras clave
programa     = "Program" 
fin_programa = "EndProgram" | "End Program"

nombre = "Eliana" | "David" | "Gabriel" | "Luis"
fin_nombre = "EndEliana" | "EndDavid" | "EndGabriel" | "EndLuis"

tipo     = "Int" | "Real"  | "String"
leer     = "Read"
escribir = "Write"

si       = "If"
entonces = "Then"
sino     = "Else"
finSi    = "EndIf" | "End If"

hacer = "Do"

mientras     = "While"
fin_mientras = "EndWhile" | "End While"

para       = "For"
hasta      = "To"
paso       = "Step"
fin_para   = "EndFor" | "End For"

segun        = "Switch"
de_otro_modo = "Otherwise"
fin_segun    = "EndSwitch" | "End Switch"


%%
{constante_alfanumerica} {ts.add(new Token("Constante Alfanumerica ", yytext())); return symbol(sym.constanteAlfanumerica, yytext());}

{programa}     {ts.add(new Token("Palabra reservada ", yytext())); return symbol(sym.programa, yytext());}
{fin_programa} {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.fin_programa, yytext());}

{nombre}     {ts.add(new Token("Palabra reservada ", yytext())); return symbol(sym.nombre, yytext());}
{fin_nombre} {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.finNombre, yytext());}

{tipo} {ts.add(new Token("Tipo de Dato", yytext())); return symbol(sym.tipo, yytext());}

{leer}     {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.leer, yytext());}
{escribir} {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.escribir, yytext());}

{si}       {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.si, yytext());}
{entonces} {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.entonces, yytext());}
{sino}     {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.sino, yytext());}
{finSi}    {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.finSi, yytext());}

{hacer} {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.hacer, yytext());}

{mientras}     {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.mientras, yytext());}
{fin_mientras} {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.finMientras, yytext());}

{para}     {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.para, yytext());}
{hasta}    {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.hasta, yytext());}
{paso}     {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.paso, yytext());}
{fin_para} {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.finPara, yytext());}

{segun}        {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.segun, yytext());}
{de_otro_modo} {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.deOtroModo, yytext());}
{fin_segun}    {ts.add(new Token("Palabra Reservada ", yytext())); return symbol(sym.finSegun, yytext());}

{parentesis_izquiedo} {ts.add(new Token("Parentesis Izquierdo ", yytext())); return symbol(sym.parentesisIzquierdo, yytext());}
{parentesis_derecho}  {ts.add(new Token("Parentesis Derecho ", yytext())); return symbol(sym.parentesisDerecho, yytext());}

{operador_aritmetico} {ts.add(new Token("operador aritmético ", yytext())); return symbol(sym.operadorAritmetico, yytext());}
{operador_logico}     {ts.add(new Token("operador logico ", yytext())); return symbol(sym.operadorLogico, yytext());}
{operador_relacional} {ts.add(new Token("Op. relacional ", yytext())); return symbol(sym.operadorRelacional, yytext());}

{punto_coma} {ts.add(new Token("punto y coma ", yytext())); return symbol(sym.puntoComa, yytext());}
{asignacion} {ts.add(new Token("Asignación ", yytext())); return symbol(sym.asignacion, yytext());}
{dos_puntos} {ts.add(new Token("Dos Puntos ", yytext())); return symbol(sym.dosPuntos, yytext());}
{coma}       {ts.add(new Token("Coma ", yytext())); return symbol(sym.coma, yytext());}

{numero}        {ts.add(new Token("Numero ", yytext())); return symbol(sym.numero, yytext());}
{identificador} {ts.add(new Token("Identificador ", yytext())); return symbol(sym.identificador, yytext());}

{espacio} {}

. {errlex+="\nError lexico: " + yytext() + " caracter no valido en pos: " + (yyline+1) + "," + (yycolumn+1);}

