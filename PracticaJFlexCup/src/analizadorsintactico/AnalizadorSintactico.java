/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package analizadorsintactico;

import java.io.File;
import java.io.FileReader;
import java.nio.file.Paths;

/**
 *
 * @author familia cj
 */
public class AnalizadorSintactico {
    public static void main(String[] args) {
        try {
            String[] parts = {"src", "analizadorsintactico", "program.txt"};
            //parts[2] = "fuente.txt";
            String ruta = Paths.get(parts[0], parts[1], parts[2]).toString();

            String archivo = new File(ruta).getAbsolutePath();
            Lexer lex = new Lexer(new FileReader(archivo));

            parser p = new parser(lex);

            p.parse();  // compila

            if (lex.errlex.isEmpty() && p.errsin.isEmpty()){
                System.out.println("Compilación correcta");
                System.out.println(lex.ts.toString());
            }
            else{
                System.err.println("Compilacion incorrecta");
                System.err.println(lex.errlex);
                System.err.println(p.errsin);
            }
        }catch(Exception e){
            System.err.println(e.getMessage());
        }
    }
}
