namespace LibraryAPI.Services
{
    public interface IAiServiceClient
    {
        Task<string> AskAsync(string question);

        Task<Stream> AskStreamAsync(string question);
    }
}