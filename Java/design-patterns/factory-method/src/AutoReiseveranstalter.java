public class AutoReiseveranstalter extends Reiseveranstalter{
    protected Fahrzeug doMakeFahrzeug(String typ){
        if (typ.equals("Golf")) {
            return new Golf();
        } else if (typ.equals("BMW")) {
            return new BMW();
        } else if (typ.equals("Ferrari")) {
            return new Ferrari();
        }else{
            return null;
        }
    }
}
