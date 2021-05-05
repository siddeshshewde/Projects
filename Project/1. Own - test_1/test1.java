public class test1
{
    public static void main (String args[])
    {
        insert();
    }

    public static Node insert()
    {
        Node head = new Node();
        Node btree = new Node(5);
        if (head.right == null)
        {
            head.right = btree;
            System.out.print("inside if else");
            return btree;
        }
        System.out.print("outside if else");
        return btree;
    } 
}