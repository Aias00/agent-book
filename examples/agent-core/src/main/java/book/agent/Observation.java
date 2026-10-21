package book.agent;

public record Observation(String question, String lastResult, int step, int remainingBudget) {}
