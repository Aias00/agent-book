package book.agent;

import java.util.Map;

public final class ToolRegistry {
    private final Map<String, Tool> tools;
    public ToolRegistry(Map<String, Tool> tools) { this.tools = Map.copyOf(tools); }
    public String execute(String name, String argument) {
        Tool tool = tools.get(name);
        if (tool == null) return "拒绝：未知工具 " + name;
        if (argument == null || argument.isBlank()) return "拒绝：参数为空";
        return tool.execute(argument);
    }
}
