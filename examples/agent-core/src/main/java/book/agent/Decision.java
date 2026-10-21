package book.agent;

public record Decision(String toolName, String argument, boolean finish) {
    public static Decision done() { return new Decision("", "", true); }
    public static Decision call(String tool, String argument) { return new Decision(tool, argument, false); }
}
