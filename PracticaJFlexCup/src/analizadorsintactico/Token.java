/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package analizadorsintactico;

public class Token {
    public String id;
    public String contenido;

    public Token(String id, String contenido) {
        this.id = id;
        this.contenido = contenido;
    }

    @Override
    public String toString() {
        return "\n" + id + "  " + contenido ;
    }
}
