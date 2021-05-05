import java.util.Scanner;
import java.util.concurrent.TimeUnit;
//import Node.Node;

public class BPlusTree
{

    static Node newElement = new Node();

    public static void main(String args[])
    {
        Scanner input = new Scanner(System.in);

        Node head = new Node();
        Node btree = new Node();
        //Node btree = new Node();
        
        while (true)
        {
            System.out.println("Choose an option:");
            System.out.println("1. Insert an Element.");
            System.out.println("2. Delete an Element.");
            System.out.println("3. Display Elements.");
            System.out.println("4. Modify an Element.");
            System.out.println("5. Exit.");

            int option = input.nextInt();
            switch(option)
            {
                case 1 : btree = insert(head, btree) ;
                break;
                case 3 : display(head, btree);
                 break;
                case 5 : exit();
            }
        }        
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

    public static Node insert(Node head, Node btree)
    {
        Scanner input = new Scanner(System.in);
        System.out.println("Enter the element to be inserted:");
        int element = input.nextInt();
        newElement.key = element;
        System.out.printf("element is: ", (int)newElement.key);

        if (head.right == null)
        {
            head.right = newElement;
            btree = newElement;
            System.out.printf("Inserted element is: ", (int)btree.key);
            return btree;
        }
        Node traverse = head;
        while(traverse.next != null)
        {
            traverse = traverse.next;
        }
        traverse.next = newElement;
        btree = traverse;
        System.out.printf("Inserted element is: ", newElement.key);
        return btree;
    }

    public static void display(Node head, Node btree)
    {
        Node traverse = head.next;
        while (traverse.next != null)
        {
            System.out.println(traverse.key);
            traverse = traverse.next;
        }
    }
}