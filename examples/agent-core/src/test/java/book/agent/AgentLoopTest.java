package book.agent;

import org.junit.jupiter.api.Test;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;
import static org.junit.jupiter.api.Assertions.*;

class AgentLoopTest {
    @Test void executesToolThenFinishes() {
        AtomicInteger calls = new AtomicInteger();
        ModelGateway model = o -> calls.getAndIncrement() == 0 ? Decision.call("echo", o.question()) : Decision.done();
        AgentLoop.Result result = new AgentLoop(model, new ToolRegistry(Map.of("echo", new EchoTool())), 3).run("你好");
        assertEquals("你好", result.answer()); assertFalse(result.budgetExhausted()); assertEquals(1, result.events().size());
    }
    @Test void stopsAtBudget() {
        ModelGateway model = o -> Decision.call("echo", "继续");
        AgentLoop.Result result = new AgentLoop(model, new ToolRegistry(Map.of("echo", new EchoTool())), 2).run("循环");
        assertTrue(result.budgetExhausted()); assertEquals(3, result.events().size());
    }
    @Test void rejectsUnknownAndBlankArguments() {
        ToolRegistry registry = new ToolRegistry(Map.of("echo", new EchoTool()));
        assertTrue(registry.execute("missing", "x").startsWith("拒绝"));
        assertTrue(registry.execute("echo", " ").startsWith("拒绝"));
    }
    private static final class EchoTool implements Tool { public String name(){return "echo";} public String execute(String argument){return argument;} }
}
