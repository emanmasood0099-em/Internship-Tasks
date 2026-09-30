using System.Net.Http.Json;
using System.Text.Json;

namespace LibraryAPI.Services
{
    public class AiServiceClient : IAiServiceClient
    {
        private readonly HttpClient _httpClient;

        public AiServiceClient(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        // Normal AI request
        public async Task<string> AskAsync(string question)
        {
            var request = new
            {
                question = question
            };

            var response = await _httpClient.PostAsJsonAsync(
                "ask",
                request
            );

            response.EnsureSuccessStatusCode();

            var result =
                await response.Content.ReadFromJsonAsync<JsonElement>();

            if (result.TryGetProperty("answer", out var answer))
            {
                return answer.GetString() ?? "";
            }

            throw new InvalidOperationException(
                "AI service returned an invalid response."
            );
        }

        // Streaming AI request
        public async Task<Stream> AskStreamAsync(string question)
        {
            var request = new HttpRequestMessage(
                HttpMethod.Post,
                "ask/stream"
            )
            {
                Content = JsonContent.Create(new
                {
                    question = question
                })
            };

            var response = await _httpClient.SendAsync(
                request,
                HttpCompletionOption.ResponseHeadersRead
            );

            response.EnsureSuccessStatusCode();

            return await response.Content.ReadAsStreamAsync();
        }
    }
}
