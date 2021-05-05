import java.util.*;
import java.lang.*;
import java.io.*;

public class bplustree
{
    int m;
    InternalNode root;
    LeafNode firstLeaf;

    public static void main(String[] args) {

		if (args.length != 1) {
			System.err.println("usage: java bplustree <file_name>");
			System.exit(-1);
		}

		String fileName = args[0];
		try {

			File file = new File(System.getProperty("user.dir") + "/" + fileName);
			Scanner sc = new Scanner(file);

			FileWriter logger = new FileWriter("output_file.txt", false);
			boolean firstLine = true;

			bplustree bpt = null;

			while (sc.hasNextLine()) {
				String line = sc.nextLine().replace(" ", "");
				String[] tokens = line.split("[(,)]");

				switch (tokens[0]) {

					case "Initialize":
						bpt = new bplustree(Integer.parseInt(tokens[1]));
						break;

					case "Insert":
						break;

					case "Delete":
						break;

					case "Search":

                    





					default:
						throw new IllegalArgumentException("\"" + tokens[0] +
								"\"" + " is an unacceptable input.");
				}
			}

			logger.close();

		} catch (FileNotFoundException e) {
			System.err.println(e);
		} catch (IllegalArgumentException e) {
			System.err.println(e);
		} catch (IOException e) {
			System.err.println(e);
		}
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
		Integer[] keys;
		Node[] childPointers;

        private InternalNode(int m, Integer[] keys) {
			this.maxDegree = m;
			this.minDegree = (int)Math.ceil(m/2.0);
			this.degree = 0;
			this.keys = keys;
			this.childPointers = new Node[this.maxDegree+1];
		}

        private InternalNode(int m, Integer[] keys, Node[] pointers) {
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
		int key;
		double value;

		public DictionaryPair(int key, double value) {
			this.key = key;
			this.value = value;
		}

		@Override
		public int compareTo(DictionaryPair o) {
			if (key == o.key) { return 0; }
			else if (key > o.key) { return 1; }
			else { return -1; }
		}
	}



    public void insert(int key, double value){
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


					Integer[] parent_keys = new Integer[this.m];
					parent_keys[0] = halfDict[0].key;
					InternalNode parent = new InternalNode(this.m, parent_keys);
					ln.parent = parent;
					parent.appendChildPointer(ln);

				} else {


					int newParentKey = halfDict[0].key;
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
}