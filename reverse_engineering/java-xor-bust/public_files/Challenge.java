import java.util.Arrays;
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;

public class Challenge {

    private String encrypt(String flag) {
        
        char [] test = flag.toCharArray();
        char [] row1 = Arrays.copyOfRange(test, 0, test.length/2);
        char [] row2 = Arrays.copyOfRange(test, test.length/2, test.length);

        int [] enc = new int[test.length];

        for(int x = 0; x < row1.length; x++)
            enc[x] = (row1[x] ^ row2[x]);

        for(int x = 0; x < row2.length; x++)    
            enc[x+row1.length] = (row2[x] + enc[x]);    

        return Arrays.toString(enc);
    }

    public static void main(String[] args) {
        Challenge c = new Challenge();
        
        String base = "";

        try {
            File inputFile = new File("flag.txt");
            Scanner s = new Scanner(inputFile);
            base = s.nextLine();
            s.close();
        } catch (FileNotFoundException e) { System.out.println("\"flag.txt\" not found."); e.printStackTrace(); }
        
        String cipher = c.encrypt(base);

        try {
            FileWriter w = new FileWriter("message.enc");
            w.write(cipher);
            w.close();
        } catch (IOException e) { System.out.println("\"message.enc\" not written."); e.printStackTrace(); }
    }
}