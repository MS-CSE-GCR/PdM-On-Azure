namespace CSharpModule
{
    using System;
    using System.IO;
    using System.Runtime.InteropServices;
    using System.Runtime.Loader;
    using System.Text;
    using System.Threading;
    using System.Threading.Tasks;

    public class DataHelper
    {
        // static string message = "{\"input_df\": [{\"sepal length\": 3.0, \"sepal width\": 3.6, \"petal width\": 1.3, \"petal length\":0.25}]}";
        //petal width: 0.1-2.5, sepal length: 4.3-7.9, sepal width: 2.0-4.4, petal length: 1.0-6.9, Timestamp, Location (Beijing, Shanghai, HK, TW, …)
        public string GetData()
        {
            string sepal_width = (new Random().Next(1, 25) / 10.0).ToString();
            string sepal_length = (new Random().Next(43, 79) / 10.0).ToString();
            string petal_width = (new Random().Next(20, 44) / 10.0).ToString();
            string petal_length = (new Random().Next(10, 69) / 10.0).ToString();
            string Timestamp = DateTime.Now.ToString();
            string Location = GetCityName(new Random().Next(0, 5));

            StringBuilder sb = new StringBuilder();
            sb.Append("{\"input_df\": [{\"sepal length\": ");
            sb.Append(sepal_width);
            sb.Append(", \"sepal width\": ");
            sb.Append(sepal_length);
            sb.Append(", \"petal width\": ");
            sb.Append(petal_width);
            sb.Append(", \"petal length\": ");
            sb.Append(petal_length);
            sb.Append(", \"Timestamp\": \"");
            sb.Append(Timestamp);
            sb.Append("\", \"Location\": \"");
            sb.Append(Location);
            sb.Append("\"}]}");
            string message = sb.ToString();

            return message;
        }

        private string GetCityName(int i)
        {
            switch (i)
            {
                case 0:
                    return "Beijing";


                case 1:
                    return "Shanghai";

                case 2:
                    return "Guangzhou";

                case 3:
                    return "Shenzhen";

                case 4:
                    return "HK";

                case 5:
                    return "TW";

                default:
                    return "Beijing";
            }
        }
    }
}