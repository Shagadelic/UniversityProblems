public class BMW implements Fahrzeug{
    public String beschreibung(){
        return "Vroom vroom";
    }
    public double preisBerechnen(double distanz){
        return distanz * 2.2;
    }
}
