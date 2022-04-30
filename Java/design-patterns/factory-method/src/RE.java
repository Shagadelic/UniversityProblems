public class RE implements Fahrzeug{
    public String beschreibung(){
        return "Der Regionalexpress tuckert durch die Gegend und hält fast überall";
    }
    public double preisBerechnen(double distanz){
        return distanz * 1.2;
    }
}
