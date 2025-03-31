using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;

public class PlayerMovement : MonoBehaviour
{
    public float speedMultiplier = 10f; // Hareket çarpanı
    public float rotationSpeed = 50f;   // Dönüş hızı çarpanı

    private UdpClient udpClient;
    private IPEndPoint endPoint;

    void Start()
    {
        // UDP bağlantısını başlat
        udpClient = new UdpClient(5052);
        endPoint = new IPEndPoint(IPAddress.Any, 5052);
    }

    void Update()
    {
        if (udpClient.Available > 0)
        {
            byte[] data = udpClient.Receive(ref endPoint);
            string message = Encoding.UTF8.GetString(data);
            string[] values = message.Split(',');

            if (values.Length == 4) // X, Y, Z hareket + Rotation
            {
                float moveX = float.Parse(values[0]) * speedMultiplier;
                float moveY = float.Parse(values[1]) * speedMultiplier;
                float moveZ = float.Parse(values[2]) * speedMultiplier;
                float rotateY = float.Parse(values[3]) * rotationSpeed;  // **Sadece EL ile ROTATE**

                // Hareketi uygula
                transform.Translate(new Vector3(moveX, moveY, moveZ) * Time.deltaTime);

                // **Sadece el hareketleriyle rotasyonu uygula**
                if (rotateY != 0) // Eğer el hareketi varsa döndür
                {
                    transform.Rotate(0, rotateY * Time.deltaTime, 0);
                }
            }
        }
    }

    private void OnApplicationQuit()
    {
        udpClient.Close();
    }
}
