package tagterm;

import java.io.*;


public final class Tagterm extends Base {

    private static final boolean VERBOSE = true;
    // If `true`, ignore HTML tidy validation warnings/errors.
    private static final boolean PERMISSIVE = true;

    private String path;

    public Tagterm(String path) {
        this.path = path;
    }

    private static String getErrMsg(int rcode) {
        String msg = "unknown";
        switch (rcode) {
            case 2:
                msg = "process";
                break;
            case 10:
                msg = "convert";
                break;
            case 20:
                msg = "remove";
                break;
            case 30:
                msg = "validate";
                break;
        }
        return msg + " error";
    }

    private String exec(String arg, boolean output) throws Exception {
        Runtime runtime = Runtime.getRuntime();
        if (VERBOSE) {
            arg = "-v " + arg;
        }
        String command = path + " " + arg;
        Process process = runtime.exec(command);
        int rcode = process.waitFor();
        InputStream is = process.getInputStream();
        BufferedReader br = new BufferedReader(
                new InputStreamReader(
                        is
                )
        );

        String line = br.readLine();

        if (rcode != 0) {
            throw new Exception(getErrMsg(rcode));
        }
        if (output && line == null) {
            throw new Exception("missing output");
        }

        return line;
    }

    private String createFile(String content, String name, String ext) throws Exception {
        File temp = File.createTempFile(name, "." + ext);
        FileOutputStream fileoutput = new FileOutputStream(temp);
        BufferedWriter buffout = new BufferedWriter(
            new OutputStreamWriter(fileoutput, ENCODING));
        buffout.write(content);
        buffout.close();
        temp.deleteOnExit();
        return temp.getPath();
    }

    public boolean validate(String file) throws Exception {
        String arg = String.format("validate -i %s", file);
        if (PERMISSIVE) {
            arg += " -pp";
        }
        exec(arg, false);
        return true;
    }

    public boolean validates(String html) throws Exception {
        String file = createFile(html, "validate", "html");
        return validate(file);
    }

    public String convert(String file) throws Exception {
        String arg = String.format("convert -i %s", file);
        if (PERMISSIVE) {
            arg += " -pp";
        }
        String out = exec(arg, true);
        return out;
    }

    public String converts(String html) throws Exception {
        String file = createFile(html, "convert", "html");
        file = convert(file);
        return getContent(file);
    }

    public String remove(String file) throws Exception {
        String arg = String.format("remove -i %s", file);
        String out = exec(arg, true);
        return out;
    }

    public String removes(String html) throws Exception {
        String file = createFile(html, "remove", "xhtml");
        file = remove(file);
        return getContent(file);
    }
}
