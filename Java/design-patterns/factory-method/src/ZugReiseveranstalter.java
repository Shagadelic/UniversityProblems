public class ZugReiseveranstalter extends Reiseveranstalter{
    protected Fahrzeug doMakeFahrzeug(String typ){
        if (typ.equals("RE")){
            return new RE();
        } else if (typ.equals("IC")) {
            return new IC();
        } else if (typ.equals("ICE")) {
            return new ICE();
        } else{
            return null;
        }
    }
}
