using System.Net;
using System.Net.NetworkInformation;
using MiniExcelLibs;

namespace ConsoleAppTest
{
    internal class PingCheck
    {
        static async Task Main(string[] args)
        {
            List<PingResult> pingResults = new List<PingResult>();

#if true
            // Get current date in yyyyMMdd format
            string currentDate = DateTime.Now.ToString("yyyyMMdd");

            // Read ip addresses from file          
            //ip.txt content like this:
            //192.168.1.1
            //192.168.2.1
            string[] lines = await File.ReadAllLinesAsync("ip.txt");
            List<IPAddress> ipAddresses = new List<IPAddress>();
            foreach (string line in lines)
            {
                string[] parts = line.Split('.');
                if (parts.Length != 4)
                {
                    // Invalid IP address format
                    continue;
                }
                int start = int.Parse(parts[3]);
                for (int i = start; i <= 254; i++)
                {
                    string ipAddressString = $"{parts[0]}.{parts[1]}.{parts[2]}.{i}";
                    IPAddress ipAddress;
                    if (IPAddress.TryParse(ipAddressString, out ipAddress))
                    {
                        ipAddresses.Add(ipAddress);
                    }
                }
            }

            // Loop through each IP address in ip_addresses.txt
            int row = 1;
            //int total = lines.Length;
            int total = ipAddresses.Count;
            int count = 0;
            var tasks = new Task[total];
            foreach (IPAddress ipAddress in ipAddresses)
            {
                tasks[count] = Task.Run(async () =>
                {
                    // Create new ping object
                    Ping ping = new Ping();

                    // Ping IP address
                    PingReply reply = await ping.SendPingAsync(ipAddress);

                    // Write IP address and ping time to worksheet
                    if (reply.Status == IPStatus.Success)
                    {
                        int currentRow = row;
                        pingResults.Add(new PingResult { IpAddr = ipAddress.ToString(), ReplyTime = reply.RoundtripTime.ToString(),CheckTime=DateTime.Now });
                        row++;
                    }
                });
                count++;
            }
            await Task.WhenAll(tasks);

#endif
            // Save Excel file with current date as filename
            string fileName = $"{currentDate}.xlsx";            
            MiniExcel.SaveAs(fileName, pingResults,overwriteFile:true);
        }

        private class PingResult
        {
            public string IpAddr { get; set; }
            public string ReplyTime { get; set; }
            public DateTime CheckTime { get; set; }
        }



    }
}
