import java.awt.geom.Point2D;
import java.util.HashMap;
import java.util.Scanner;

public abstract class Reiseveranstalter {
    //Factory methode
    protected abstract Fahrzeug doMakeFahrzeug(String typ);
    public double berechnePreis(String typ, String stadt1, String stadt2){
        //Beispiel Koordinaten mit lineal von Bad Hersfeld aus
        Point2D berlin = new Point2D.Double(10.5,8.5);
        Point2D hamburg = new Point2D.Double(0.5,13);
        Point2D dortmund = new Point2D.Double(-6.5,4);
        Point2D köln = new Point2D.Double(-8.5,0.5);
        Point2D münchen = new Point2D.Double(5,-13);
        Point2D leipzig = new Point2D.Double(8.5,2.5);

        HashMap<String, Point2D> hm = new HashMap<String, Point2D>();
        hm.put("Berlin", berlin);
        hm.put("Hamburg", hamburg);
        hm.put("Dortmund", dortmund);
        hm.put("Köln", köln);
        hm.put("München", münchen);
        hm.put("Leipzig", leipzig);
        double distanz = eucDistance(hm.get(stadt1), hm.get(stadt2));
        Fahrzeug fahrzeug = doMakeFahrzeug(typ);
        System.out.println(fahrzeug.beschreibung());

        return fahrzeug.preisBerechnen(distanz);
    }
    public double eucDistance(Point2D a, Point2D b) {
        double dx = a.getX() - b.getX();
        double dy = a.getY() - b.getY();
        return Math.sqrt(dx*dx + dy*dy);
    }

    public static void main(String[] args) {
        Scanner read = new Scanner(System.in);
        System.out.println("Auswahl Fahrzeugklasse:"+"\n"+"Zug"+"\n"+"Auto");
        String wahl1 = read.nextLine();
        System.out.println(wahl1);

        if (wahl1.equals("Zug")){
            Reiseveranstalter veranstalter = new ZugReiseveranstalter();
            System.out.println("Auswahl Fahrzeug:"+"\n"+"RE"+"\n"+"IC"+"\n"+"ICE");

            String wahl2 = read.nextLine();
            System.out.println(wahl2);
            System.out.println("Wahl 2 Städte"+"\n"+"Berlin, Hamburg, Dortmund, Köln, München und Leipzig");
            String wahl3 = read.nextLine();
            String wahl4 = read.nextLine();
            System.out.println(wahl3 +" "+ wahl4);

            double preis = veranstalter.berechnePreis(wahl2, wahl3, wahl4);
            System.out.println("Preis: "+preis);
        }else {
            Reiseveranstalter veranstalter = new AutoReiseveranstalter();
            System.out.println("Auswahl Fahrzeug:"+"\n"+"Golf"+"\n"+"BMW"+"\n"+"Ferrari");

            String wahl2 = read.nextLine();
            System.out.println(wahl2);
            System.out.println("Wahl 2 Städte"+"\n"+"Berlin, Hamburg, Dortmund, Köln, München und Leipzig");
            String wahl3 = read.nextLine();
            String wahl4 = read.nextLine();
            System.out.println(wahl3 +" "+ wahl4);

            double preis = veranstalter.berechnePreis(wahl2, wahl3, wahl4);
            System.out.println("Preis: "+preis);
        }

    }
}
