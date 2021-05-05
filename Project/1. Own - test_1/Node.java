public class Node {

	int key;
	Node left, right, next;

	public Node()
	{
		this.left = null;
		this.right = null;
		this.next = null;
		key = 0;
	}

	public Node(int data)
	{
		System.out.println("here");
		key = data;
		this.left = null;
		this.right = null;
		this.next = null;
		System.out.println("element added...");
		System.out.println(key);
	}

}
