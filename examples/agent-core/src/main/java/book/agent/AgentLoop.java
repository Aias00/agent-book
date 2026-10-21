package book.agent;

import java.util.ArrayList;
import java.util.List;

public final class AgentLoop {
    private final ModelGateway model;
    private final ToolRegistry tools;
    private final int maxSteps;
    public AgentLoop(ModelGateway model, ToolRegistry tools, int maxSteps) {
        if (maxSteps < 1) throw new IllegalArgumentException("maxSteps must be positive");
        this.model = model; this.tools = tools; this.maxSteps = maxSteps;
    }
    public Result run(String question) {
        String last = ""; List<String> events = new ArrayList<>();
        for (int step = 0; step < maxSteps; step++) {
            Decision decision = model.decide(new Observation(question, last, step, maxSteps - step));
            if (decision.finish()) return new Result(last, events, false);
            last = tools.execute(decision.toolName(), decision.argument());
            events.add("step=" + step + " tool=" + decision.toolName() + " result=" + last);
        }
        events.add("budget_exhausted");
        return new Result(last, events, true);
    }
    public record Result(String answer, List<String> events, boolean budgetExhausted) {}
}
