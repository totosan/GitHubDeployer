public class SimulationCommand : ISimulationCommand
{
    public long RunId { get; set; }
    public string Command { get; set; }
    public int Value { get ;set; }
}