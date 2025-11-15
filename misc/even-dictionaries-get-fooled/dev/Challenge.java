import java.util.Scanner;
import java.util.Random;

public class Challenge {
    public static void main(String[] args) {
        
        Scanner keyboard = new Scanner(System.in);
        Random rand = new Random(System.currentTimeMillis());

        System.out.println("Welcome to my custom dictionary!");
        System.out.println("I can proudly say this is the first dictionary where the size of the data structure is randomly chosen!");
        System.out.println("(btw, I have a tiny computer, so I use double hashing to save on resources.)\n");

        int size = rand.nextInt(20) * 2 + 10;
        Dictionary d = new Dictionary(size);
        
        System.out.println("Dictionary size randomly assigned to... " + size);
        System.out.println("If you can convince my dictionary that it is full, it'll give you the flag. But, to save on resources you can only enter 3 values. I hope you understand.");


        int choice = -1;
        int entries = 3;
        while(true) {
            do {
                
                System.out.println("\nYou have " + entries + " insertions remaining.");
                System.out.println("1: View Hashmap");
                System.out.println("2: Add Value to Hashmap");
                System.out.println("3: View Keying/Hashing Algorithm");
                System.out.print("Enter Choice:\t> ");
                choice = keyboard.nextInt();
                clearScreen();
                
            } while(choice < 1 || choice > 3);

            switch(choice) {
                case 1:
                    
                    d.printDict();
                    break;

                case 2:
                    
                    if(entries > 0) {
                    System.out.println("Add New Value");
                    System.out.print("Enter key:\t> ");
                    String inp_key = keyboard.next();
                    System.out.print("Enter value:\t> ");
                    String inp_value = keyboard.next();
                    d.insert(inp_key, inp_value);
                    entries--;
                    }
                    else {
                        System.out.println("Sorry, you've run out of insertions. Glad to hear my dictionary can handle 3 values!");
                        System.exit(0);
                    }
                    break;

                case 3:
                    System.out.println("Hashmap / Dictionary Basics:");
                    System.out.println("Dictionaries store objects with a key-value pair. To add to a dictionary, you provide both a value and a key to find that value.");
                    System.out.println("The key gets hashed, and the location in which the value is stored is derived from the hash of the key.");
		    System.out.println("\nMy Keying and Hashing Algorithm:\n");                    
		System.out.println("        private int getKey(String inp_key) {");
		System.out.println("                char[] ch = inp_key.toCharArray();");
		System.out.println("                int value = 0;");
		System.out.println("");
		System.out.println("                for(char c : ch) {");
		System.out.println("                        value += c;");
		System.out.println("                }");
		System.out.println("                return value;");
		System.out.println("        }");
		System.out.println("");
		System.out.println("        // n is size of dictionary");
		System.out.println("        // https://www.educative.io/answers/what-is-double-hashing");
		System.out.println("");
		System.out.println("        private int[] hash(int key) {");
		System.out.println("                int hash1, hash2;");
		System.out.println("                hash1 = key % n;");
		System.out.println("");
		System.out.println("                for(hash2 = 0; key != 0; key /= 10) {");
		System.out.println("                        hash2 += key % 10;");
		System.out.println("                }");
		System.out.println("                return new int[]{hash1, hash2};");
      		System.out.println("        }");
 		    break;
            }
        }
    }

    public static void clearScreen() {  
        System.out.print("\033[H\033[2J");  
        System.out.flush();  
    }  
}
