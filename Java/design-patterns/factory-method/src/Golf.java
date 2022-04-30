public class Golf implements Fahrzeug{
    public String beschreibung(){
        return "Vroom";
    }
    public double preisBerechnen(double distanz){
        return distanz * 1.8;
    }
}
