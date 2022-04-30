import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;


public class GUI extends JFrame implements ActionListener {
    Zaehlsteuerung z1;
    Zaehlsteuerung z2;
    Display disp;
    JPanel pointContainer;
    JPanel buttonContainer1;
    JPanel buttonContainer2;
    JButton incrementH1;
    JButton incrementG1;
    JButton reset1;
    JButton incrementH2;
    JButton incrementG2;
    JButton reset2;

    JLabel heimLabel;
    JLabel gastLabel;
    GUI(Zaehlsteuerung z1, Zaehlsteuerung z2, Display d){
        this.z1 = z1;
        this.z2 = z2;
        this.disp = d;
        this.setVisible(true);
        this.setTitle("Zaehlanlage GUI");
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        this.setLayout(new GridLayout(3,2));
        pointContainer = new JPanel();
        buttonContainer1 = new JPanel();
        buttonContainer2 = new JPanel();

        heimLabel  = new JLabel("HEIM: 0");
        gastLabel  = new JLabel("GAST: 0");

        JLabel lab1 = new JLabel("Controls 1 ");
        JLabel lab2 = new JLabel("Controls 2 ");

        incrementH1 = new JButton();
        incrementG1 = new JButton();
        reset1 = new JButton();

        incrementH1.setText("H +");
        incrementG1.setText("G +");
        reset1.setText("RESET");

        incrementH2 = new JButton();
        incrementG2 = new JButton();
        reset2 = new JButton();

        incrementH2.setText("H +");
        incrementG2.setText("G +");
        reset2.setText("RESET");

        incrementH1.addActionListener(this);
        incrementG1.addActionListener(this);
        reset1.addActionListener(this);

        incrementH2.addActionListener(this);
        incrementG2.addActionListener(this);
        reset2.addActionListener(this);

        pointContainer.add(heimLabel);
        pointContainer.add(gastLabel);

        buttonContainer1.add(lab1);
        buttonContainer1.add(incrementH1);
        buttonContainer1.add(incrementG1);
        buttonContainer1.add(reset1);

        buttonContainer2.add(lab2);
        buttonContainer2.add(incrementH2);
        buttonContainer2.add(incrementG2);
        buttonContainer2.add(reset2);

        this.add(pointContainer);
        this.add(buttonContainer1);
        this.add(buttonContainer2);

        this.pack();
    }

    @Override
    public void actionPerformed(ActionEvent e){
        if(e.getSource() == incrementH1){
            z1.erhoeheHeim();
            heimLabel.setText("HEIM: "+disp.getHeim());
        }else if (e.getSource() == incrementG1){
            z1.erhoeheGast();
            gastLabel.setText("GAST: "+disp.getGast());
        }else if (e.getSource() == reset1){
            z1.reset();
            heimLabel.setText("HEIM: "+disp.getHeim());
            gastLabel.setText("GAST: "+disp.getGast());
        }else if(e.getSource() == incrementH2){
            z2.erhoeheHeim();
            heimLabel.setText("HEIM: "+disp.getHeim());
        }else if (e.getSource() == incrementG2){
            z2.erhoeheGast();
            gastLabel.setText("GAST: "+disp.getGast());
        }else if (e.getSource() == reset2){
            z2.reset();
            heimLabel.setText("HEIM: "+disp.getHeim());
            gastLabel.setText("GAST: "+disp.getGast());
        }
    }
}
