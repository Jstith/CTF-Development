public class Dictionary {

	private String[] dict_primary;
	private int n; // Length of dictionary

	public Dictionary(int inp_size) {
        n = inp_size;
		dict_primary = new String[n];
	}

	private int getKey(String inp_node) {
		char[] ch = inp_node.toCharArray();
		int value = 0;

		for(char c : ch) {
			value += c;
		}
		return value;
	}

	private int[] hash(int key) {
		int hash1, hash2;
		hash1 = key % n;

		for(hash2 = 0; key != 0; key /= 10) {
			hash2 += key % 10;
		}
		return new int[]{hash1, hash2};
	}

	public void insert(String inp_key, String inp_node) {
		int key = getKey(inp_key);
		int[] hashes = hash(key);
		int indexAddress = hashes[0];

		if(inp_key.length() > 10) {
			inp_key = inp_key.substring(0, 7) + "...";
		}
		if(inp_node.length() > 10) {
			inp_node = inp_node.substring(0,7) + "...";
		}
		
		for(int x = 0; x < n; x++) {
			indexAddress += hashes[1];
			indexAddress = indexAddress % n;
			
			if(dict_primary[indexAddress] == null) {
				// Does not change the value of the hashes, just formats the string for verbose display
				String builder = String.format("%-10.10s\t%-10.10s\t(%03d + %01d * %03d) %% %02d", inp_key, inp_node, hashes[0], (x+1), hashes[1], n);
				dict_primary[indexAddress] = builder;
				return;
			}
		}
		// Dictionary must be full...
		System.out.println("Insertion Attempts exceeded size of dictionary... must be totally full.");
		System.out.println("cga{pr1m3_numb3r$_ar3_A_PR1ME_ch01c3_4_d1cT10n@r13s}");
		return;
	}

	public void printDict() {
		System.out.println("Printing Dictionary:");
		System.out.println("n:   key:      \t value:    \tIndexing Math:");
		
		for(int x = 0; x < n; x++) {
			System.out.print(String.format("%03d: ", x));
			System.out.print(dict_primary[x] + "\n");
		}
	}
}
