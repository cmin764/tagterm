import tagterm.Tagterm;


public class Main {

    private static void print(String text) {
        System.out.println(text);
    }

    public static void main(String[] args)
    {
        if (args.length < 2) {
            print("Usage: java Main EXEC HTML");
            return;
        }
        String exec = args[0].toString();
        String html = args[1].toString();

        // Create a new `tagterm` object using a path to the Python executable.
        Tagterm tagterm = new Tagterm(exec);

        // Validate the content of an HTML file.
        boolean resp = tagterm.validate(html);

        // Convert a HTML file to XHTML.


        // Remove tags with XHTML and output XML.
    }
}
