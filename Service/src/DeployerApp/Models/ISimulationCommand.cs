public interface ISimulationCommand
{
    long RunId { get; set; }
    string Command { get; set; }
    int Value { get; set; }
}