import java.lang.*;
import java.util.*;
import java.io.*;

public class bplustree {
	int m;
	InternalNode root;
	LeafNode firstLeaf;


	private int binarySearch(DictionaryPair[] dps, int numPairs, String t) {

		Comparator<DictionaryPair> c = new Comparator<DictionaryPair>() {
			@Override
			public int compare(DictionaryPair o1, DictionaryPair o2) {
				String key1 = o1.key;
				String key2 = o2.key;
				return key1.compareTo(key2);
			}
		};
		return Arrays.binarySearch(dps, 0, numPairs, new DictionaryPair(t, ""), c);
	}

	private LeafNode findLeafNode(String key) {

		String[] keys = this.root.keys;
		int i;

		for (i = 0; i < this.root.degree - 1; i++) {
			if (key.compareTo(keys[i]) < 0 ) { break; }
		}

		Node child = this.root.childPointers[i];
		if (child instanceof LeafNode) {
			return (LeafNode)child;
		} else {
			return findLeafNode((InternalNode)child, key);
		}
	}

	private LeafNode findLeafNode(InternalNode node, String key) {

		String[] keys = node.keys;
		int i;

		for (i = 0; i < node.degree - 1; i++) {
			if (key.compareTo(keys[i]) < 0 ) { break; }

		}

		Node childNode = node.childPointers[i];
		if (childNode instanceof LeafNode) {
			return (LeafNode)childNode;
		} else {
			return findLeafNode((InternalNode)node.childPointers[i], key);
		}
	}

	private int findIndexOfPointer(Node[] pointers, LeafNode node) {
		int i;
		for (i = 0; i < pointers.length; i++) {
			if (pointers[i] == node) { break; }
		}
		return i;
	}

	private int getMidpoint() {
		return (int)Math.ceil((this.m + 1) / 2.0) - 1;
	}

	private void handleDeficiency(InternalNode in) {

		InternalNode sibling;
		InternalNode parent = in.parent;

		if (this.root == in) {
			for (int i = 0; i < in.childPointers.length; i++) {
				if (in.childPointers[i] != null) {
					if (in.childPointers[i] instanceof InternalNode) {
						this.root = (InternalNode)in.childPointers[i];
						this.root.parent = null;
					} else if (in.childPointers[i] instanceof LeafNode) {
						this.root = null;
					}
				}
			}
		}

		else if (in.leftSibling != null && in.leftSibling.isLendable()) {
			sibling = in.leftSibling;
		} else if (in.rightSibling != null && in.rightSibling.isLendable()) {
			sibling = in.rightSibling;

			String borrowedKey = sibling.keys[0];
			Node pointer = sibling.childPointers[0];

			in.keys[in.degree - 1] = parent.keys[0];
			in.childPointers[in.degree] = pointer;

			parent.keys[0] = borrowedKey;

			sibling.removePointer(0);
			Arrays.sort(sibling.keys);
			sibling.removePointer(0);
			shiftDown(in.childPointers, 1);
		}

		else if (in.leftSibling != null && in.leftSibling.isMergeable()) {

		} else if (in.rightSibling != null && in.rightSibling.isMergeable()) {
			sibling = in.rightSibling;

			sibling.keys[sibling.degree - 1] = parent.keys[parent.degree - 2];
			Arrays.sort(sibling.keys, 0, sibling.degree);
			parent.keys[parent.degree - 2] = null;

			for (int i = 0; i < in.childPointers.length; i++) {
				if (in.childPointers[i] != null) {
					sibling.prependChildPointer(in.childPointers[i]);
					in.childPointers[i].parent = sibling;
					in.removePointer(i);
				}
			}

			parent.removePointer(in);

			sibling.leftSibling = in.leftSibling;
		}

		if (parent != null && parent.isDeficient()) {
			handleDeficiency(parent);
		}
	}

	private boolean isEmpty() {
		return firstLeaf == null;
	}

	private int linearNullSearch(DictionaryPair[] dps) {
		for (int i = 0; i <  dps.length; i++) {
			if (dps[i] == null) { return i; }
		}
		return -1;
	}

	private int linearNullSearch(Node[] pointers) {
		for (int i = 0; i <  pointers.length; i++) {
			if (pointers[i] == null) { return i; }
		}
		return -1;
	}

	private void shiftDown(Node[] pointers, int amount) {
		Node[] newPointers = new Node[this.m + 1];
		for (int i = amount; i < pointers.length; i++) {
			newPointers[i - amount] = pointers[i];
		}
		pointers = newPointers;
	}

	private void sortDictionary(DictionaryPair[] dictionary) {
		Arrays.sort(dictionary, new Comparator<DictionaryPair>() {
			@Override
			public int compare(DictionaryPair o1, DictionaryPair o2) {
				if (o1 == null && o2 == null) { return 0; }
				if (o1 == null) { return 1; }
				if (o2 == null) { return -1; }
				return o1.compareTo(o2);
			}
		});
	}

	private Node[] splitChildPointers(InternalNode in, int split) {

		Node[] pointers = in.childPointers;
		Node[] halfPointers = new Node[this.m + 1];

		for (int i = split + 1; i < pointers.length; i++) {
			halfPointers[i - split - 1] = pointers[i];
			in.removePointer(i);
		}

		return halfPointers;
	}

	private DictionaryPair[] splitDictionary(LeafNode ln, int split) {

		DictionaryPair[] dictionary = ln.dictionary;

		DictionaryPair[] halfDict = new DictionaryPair[this.m];

		for (int i = split; i < dictionary.length; i++) {
			halfDict[i - split] = dictionary[i];
			ln.delete(i);
		}

		return halfDict;
	}

	private void splitInternalNode(InternalNode in) {

		InternalNode parent = in.parent;

		int midpoint = getMidpoint();
		String newParentKey = in.keys[midpoint];
		String[] halfKeys = splitKeys(in.keys, midpoint);
		Node[] halfPointers = splitChildPointers(in, midpoint);

		in.degree = linearNullSearch(in.childPointers);

		InternalNode sibling = new InternalNode(this.m, halfKeys, halfPointers);
		for (Node pointer : halfPointers) {
			if (pointer != null) { pointer.parent = sibling; }
		}

		sibling.rightSibling = in.rightSibling;
		if (sibling.rightSibling != null) {
			sibling.rightSibling.leftSibling = sibling;
		}
		in.rightSibling = sibling;
		sibling.leftSibling = in;

		if (parent == null) {

			String[] keys = new String[this.m];
			keys[0] = newParentKey;
			InternalNode newRoot = new InternalNode(this.m, keys);
			newRoot.appendChildPointer(in);
			newRoot.appendChildPointer(sibling);
			this.root = newRoot;

			in.parent = newRoot;
			sibling.parent = newRoot;

		} else {

			parent.keys[parent.degree - 1] = newParentKey;
			Arrays.sort(parent.keys, 0, parent.degree);

			int pointerIndex = parent.findIndexOfPointer(in) + 1;
			parent.insertChildPointer(sibling, pointerIndex);
			sibling.parent = parent;
		}
	}

	private String[] splitKeys(String[] keys, int split) {

		String[] halfKeys = new String[this.m];

		keys[split] = null;

		for (int i = split + 1; i < keys.length; i++) {
			halfKeys[i - split - 1] = keys[i];
			keys[i] = null;
		}

		return halfKeys;
	}


	public void delete(String key) {
		if (isEmpty()) {


			System.err.println("Invalid Delete: The B+ tree is currently empty.");

		} else {

			LeafNode ln = (this.root == null) ? this.firstLeaf : findLeafNode(key);
			int dpIndex = binarySearch(ln.dictionary, ln.numPairs, key);


			if (dpIndex < 0) {


				System.err.println("Invalid Delete: Key unable to be found.");

			} else {

				ln.delete(dpIndex);

				if (ln.isDeficient()) {

					LeafNode sibling;
					InternalNode parent = ln.parent;

					if (ln.leftSibling != null &&
						ln.leftSibling.parent == ln.parent &&
						ln.leftSibling.isLendable()) {

						sibling = ln.leftSibling;
						DictionaryPair borrowedDP = sibling.dictionary[sibling.numPairs - 1];

						ln.insert(borrowedDP);
						sortDictionary(ln.dictionary);
						sibling.delete(sibling.numPairs - 1);

						int pointerIndex = findIndexOfPointer(parent.childPointers, ln);
						String borrowedDPKey = borrowedDP.key;
						String parentKey = parent.keys[pointerIndex - 1];
						
						if (!(borrowedDPKey.compareTo(parentKey) >= 0)) {
							parent.keys[pointerIndex - 1] = ln.dictionary[0].key;
						}

					} else if (ln.rightSibling != null &&
							   ln.rightSibling.parent == ln.parent &&
							   ln.rightSibling.isLendable()) {

						sibling = ln.rightSibling;
						DictionaryPair borrowedDP = sibling.dictionary[0];

						ln.insert(borrowedDP);
						sibling.delete(0);
						sortDictionary(sibling.dictionary);

						String borrowedDPKey1 = borrowedDP.key;
						int pointerIndex = findIndexOfPointer(parent.childPointers, ln);
						if (!(borrowedDPKey1.compareTo(parent.keys[pointerIndex]) < 0 )) {
							parent.keys[pointerIndex] = sibling.dictionary[0].key;
						}

					}

					else if (ln.leftSibling != null &&
							 ln.leftSibling.parent == ln.parent &&
							 ln.leftSibling.isMergeable()) {

						sibling = ln.leftSibling;
						int pointerIndex = findIndexOfPointer(parent.childPointers, ln);

						parent.removeKey(pointerIndex - 1);
						parent.removePointer(ln);

						sibling.rightSibling = ln.rightSibling;

						if (parent.isDeficient()) {
							handleDeficiency(parent);
						}

					} else if (ln.rightSibling != null &&
							   ln.rightSibling.parent == ln.parent &&
							   ln.rightSibling.isMergeable()) {

						sibling = ln.rightSibling;
						int pointerIndex = findIndexOfPointer(parent.childPointers, ln);

						parent.removeKey(pointerIndex);
						parent.removePointer(pointerIndex);

						sibling.leftSibling = ln.leftSibling;
						if (sibling.leftSibling == null) {
							firstLeaf = sibling;
						}

						if (parent.isDeficient()) {
							handleDeficiency(parent);
						}
					}

				} else if (this.root == null && this.firstLeaf.numPairs == 0) {


					this.firstLeaf = null;

				} else {

					sortDictionary(ln.dictionary);

				}
			}
		}
	}

	public void insert(String key, String value){
		if (isEmpty()) {


			LeafNode ln = new LeafNode(this.m, new DictionaryPair(key, value));

			this.firstLeaf = ln;

		} else {

			LeafNode ln = (this.root == null) ? this.firstLeaf :
												findLeafNode(key);

			if (!ln.insert(new DictionaryPair(key, value))) {

				ln.dictionary[ln.numPairs] = new DictionaryPair(key, value);
				ln.numPairs++;
				sortDictionary(ln.dictionary);

				int midpoint = getMidpoint();
				DictionaryPair[] halfDict = splitDictionary(ln, midpoint);

				if (ln.parent == null) {


					String[] parent_keys = new String[this.m];
					parent_keys[0] = halfDict[0].key;
					InternalNode parent = new InternalNode(this.m, parent_keys);
					ln.parent = parent;
					parent.appendChildPointer(ln);

				} else {


					String newParentKey = halfDict[0].key;
					ln.parent.keys[ln.parent.degree - 1] = newParentKey;
					Arrays.sort(ln.parent.keys, 0, ln.parent.degree);
				}

				LeafNode newLeafNode = new LeafNode(this.m, halfDict, ln.parent);

				int pointerIndex = ln.parent.findIndexOfPointer(ln) + 1;
				ln.parent.insertChildPointer(newLeafNode, pointerIndex);

				newLeafNode.rightSibling = ln.rightSibling;
				if (newLeafNode.rightSibling != null) {
					newLeafNode.rightSibling.leftSibling = newLeafNode;
				}
				ln.rightSibling = newLeafNode;
				newLeafNode.leftSibling = ln;

				if (this.root == null) {

					this.root = ln.parent;

				} else {

					InternalNode in = ln.parent;
					while (in != null) {
						if (in.isOverfull()) {
							splitInternalNode(in);
						} else {
							break;
						}
						in = in.parent;
					}
				}
			}
		}
	}

	public String search(String key) {

		if (isEmpty()) { return null; }

		LeafNode ln = (this.root == null) ? this.firstLeaf : findLeafNode(key);

		DictionaryPair[] dps = ln.dictionary;
		int index = binarySearch(dps, ln.numPairs, key);

		if (index < 0) {
			return null;
		} else {
			return dps[index].value;
		}
	}


	public bplustree(int m) {
		this.m = m;
		this.root = null;
	}

	public class Node {
		InternalNode parent;
	}

	private class InternalNode extends Node {
		int maxDegree;
		int minDegree;
		int degree;
		InternalNode leftSibling;
		InternalNode rightSibling;
		String[] keys;
		Node[] childPointers;

		private void appendChildPointer(Node pointer) {
			this.childPointers[degree] = pointer;
			this.degree++;
		}

		private int findIndexOfPointer(Node pointer) {
			for (int i = 0; i < childPointers.length; i++) {
				if (childPointers[i] == pointer) { return i; }
			}
			return -1;
		}

		private void insertChildPointer(Node pointer, int index) {
			for (int i = degree - 1; i >= index ;i--) {
				childPointers[i + 1] = childPointers[i];
			}
			this.childPointers[index] = pointer;
			this.degree++;
		}

		private boolean isDeficient() {
			return this.degree < this.minDegree;
		}

		private boolean isLendable() { return this.degree > this.minDegree; }

		private boolean isMergeable() { return this.degree == this.minDegree; }

		private boolean isOverfull() {
			return this.degree == maxDegree + 1;
		}

		private void prependChildPointer(Node pointer) {
			for (int i = degree - 1; i >= 0 ;i--) {
				childPointers[i + 1] = childPointers[i];
			}
			this.childPointers[0] = pointer;
			this.degree++;
		}

		private void removeKey(int index) { this.keys[index] = null; }

		private void removePointer(int index) {
			this.childPointers[index] = null;
			this.degree--;
		}

		private void removePointer(Node pointer) {
			for (int i = 0; i < childPointers.length; i++) {
				if (childPointers[i] == pointer) { this.childPointers[i] = null; }
			}
			this.degree--;
		}

		private InternalNode(int m, String[] keys) {
			this.maxDegree = m;
			this.minDegree = (int)Math.ceil(m/2.0);
			this.degree = 0;
			this.keys = keys;
			this.childPointers = new Node[this.maxDegree+1];
		}

		private InternalNode(int m, String[] keys, Node[] pointers) {
			this.maxDegree = m;
			this.minDegree = (int)Math.ceil(m/2.0);
			this.degree = linearNullSearch(pointers);
			this.keys = keys;
			this.childPointers = pointers;
		}
	}

	public class LeafNode extends Node {
		int maxNumPairs;
		int minNumPairs;
		int numPairs;
		LeafNode leftSibling;
		LeafNode rightSibling;
		DictionaryPair[] dictionary;

		public void delete(int index) {

			this.dictionary[index] = null;

			numPairs--;
		}

		public boolean insert(DictionaryPair dp) {
			if (this.isFull()) {


				return false;
			} else {

				this.dictionary[numPairs] = dp;
				numPairs++;
				Arrays.sort(this.dictionary, 0, numPairs);

				return true;
			}
		}

		public boolean isDeficient() { return numPairs < minNumPairs; }

		public boolean isFull() { return numPairs == maxNumPairs; }

		public boolean isLendable() { return numPairs > minNumPairs; }

		public boolean isMergeable() {
			return numPairs == minNumPairs;
		}

		public LeafNode(int m, DictionaryPair dp) {
			this.maxNumPairs = m - 1;
			this.minNumPairs = (int)(Math.ceil(m/2) - 1);
			this.dictionary = new DictionaryPair[m];
			this.numPairs = 0;
			this.insert(dp);
		}

		public LeafNode(int m, DictionaryPair[] dps, InternalNode parent) {
			this.maxNumPairs = m - 1;
			this.minNumPairs = (int)(Math.ceil(m/2) - 1);
			this.dictionary = dps;
			this.numPairs = linearNullSearch(dps);
			this.parent = parent;
		}
	}

	public class DictionaryPair implements Comparable<DictionaryPair> {
		String key;
		String value;

		public DictionaryPair(String key, String value) {
			this.key = key;
			this.value = value;
		}

		@Override
		public int compareTo(DictionaryPair o) {
			return key.compareTo(o.key);
		}
	}

	//Sid Check
	public void createTree()
	{
		System.out.print("Enter the filename: ");

	}

	public static void sleep(int seconds)
    {
        int ms = seconds * 1000;
        try
        {
            Thread.sleep(ms);
        }
        catch(InterruptedException ex)
        {
            Thread.currentThread().interrupt();
        }
    }

	public static void exit()
    {
        System.out.println("Closing the application.");
        sleep(1);
        System.out.print(".");
        sleep(1);
        System.out.print(".");
        sleep(1);
        System.out.print(".");
        sleep(1);
        System.exit(0);
    }

	public static void main(String[] args) 
	{
		bplustree bpt = null;

		while (true)
        {
			
            System.out.println("1. Create a B Plus Tree from File.");
            System.out.println("2. Insert an Element.");
            System.out.println("3. Delete an Element.");
            System.out.println("4. Display Elements.");
            System.out.println("5. Modify an Element.");
            System.out.println("6. Exit.");
            System.out.print("Choose an option: ");

			Scanner input = new Scanner(System.in);
            int option = input.nextInt();

            switch(option)
            {
				case 1 : 
					System.out.print("Enter the filename: ");
					input.nextLine();
					String fileName = input.nextLine();

					if (fileName.length() < 1) {
						System.err.println("Please make sure the input file is in same directory");
						System.exit(-1);
					}
					int numberOfNodes = 0;
			
					try 
					{
			
						File file = new File(System.getProperty("user.dir") + "/" + fileName);
						Scanner sc = new Scanner(file);
			
						bpt = new bplustree(3);
			
						System.out.println("***** Creating Tree *****");
						
						while (sc.hasNextLine()) 
						{
							String line = sc.nextLine();
							String[] keyAndValues = line.split("\\s{8}"); // split the string on spaces, obeys spaces as per partfile.txt
							
							numberOfNodes++;
							bpt.insert(keyAndValues[0], keyAndValues[1]);
						}
					} catch (FileNotFoundException e) {
						System.err.println(e);
					} catch (IllegalArgumentException e) {
						System.err.println(e);
					}
						
						System.out.println("***** Done Creating Tree *****");
						System.out.println("Total Number of Nodes created: " + numberOfNodes);
		
                case 2 : //head = insert(head);
                break;
                case 3 : 
				System.out.print("Enter the key to be searched: ");
				input.nextLine();
				String searchKey = input.nextLine();
				System.out.println("Key: "+ searchKey + "\nValue: " +bpt.search(searchKey));
                break;
                case 6 : exit();
            }
        }   
	}
}
