using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;

public class PlayerMovement : MonoBehaviour
{
    public float speedMultiplier = 10f;   // Multiplier for movement speed
    public float rotationSpeed = 50f;     // Multiplier for rotation speed

    private UdpClient udpClient;
    private IPEndPoint endPoint;

    void Start()
    {
        // Start listening to UDP on port 5052
        udpClient = new UdpClient(5052);
        endPoint = new IPEndPoint(IPAddress.Any, 5052);
    }

    void Update()
    {
        // Check for incoming UDP data
        if (udpClient.Available > 0)
        {
            byte[] data = udpClient.Receive(ref endPoint);
            string message = Encoding.UTF8.GetString(data);
            string[] values = message.Split(',');

            // Expecting 4 values: moveX, moveY, moveZ, rotateY
            if (values.Length == 4)
            {
                float moveX = float.Parse(values[0]) * speedMultiplier;
                float moveY = float.Parse(values[1]) * speedMultiplier;
                float moveZ = float.Parse(values[2]) * speedMultiplier;
                float rotateY = float.Parse(values[3]) * rotationSpeed;

                // Apply movement to the object
                transform.Translate(new Vector3(moveX, moveY, moveZ) * Time.deltaTime);

                // Apply rotation only if hand movement is detected
                if (rotateY != 0)
                {
                    transform.Rotate(0, rotateY * Time.deltaTime, 0);
                }
            }
        }
    }

    void OnApplicationQuit()
    {
        // Clean up the UDP connection
        udpClient.Close();
    }
}
