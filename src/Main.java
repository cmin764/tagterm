import tagterm.*;


public final class Main extends Base {

    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            print("Usage: java Main EXEC FILE");
            return;
        }
        String exec = args[0].toString();
        String file = args[1].toString();

        // Create a new `tagterm` object using a path to the Python executable.
        Tagterm tagterm = new Tagterm(exec);

        // Validate the content of an HTML file.
        boolean validate_resp = tagterm.validate(file);
        print("validate: " + validate_resp);
        boolean validates_resp = tagterm.validates(getContent(file));
        print("validates: " + validates_resp);

        // Convert a HTML file to XHTML.
        String converted_file = tagterm.convert(file);
        print("convert: " + converted_file);
        String converted_content = tagterm.converts(getContent(file));
        print("converts: " + converted_content);

        // Remove tags within XHTML and output XML.
        String removed_file = tagterm.remove(converted_file);
        print("remove: " + removed_file);
        String removed_content = tagterm.removes(getContent(converted_file));
        print("removes: " + removed_content);
    }
}
