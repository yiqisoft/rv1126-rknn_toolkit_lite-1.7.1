package main

import (
	"fmt"
	"io/ioutil"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

func main() {
	const TOPIC = "tfdemo"

	images := []string{
		"parrot.jpg",
		"owl.jpg",
		"image.jpeg",
		"out.jpg",
		// 其他你需要的图像
	}
	opts := mqtt.NewClientOptions().AddBroker("tcp://192.168.120.207:1883")
	client := mqtt.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}
	for _, image := range images {
		fmt.Println("Publishing " + image)
		payload, err := ioutil.ReadFile(image)
		if err != nil {
			fmt.Println(err)
			continue
		}
		if token := client.Publish(TOPIC, 0, false, payload); token.Wait() && token.Error() != nil {
			fmt.Println(token.Error())
		} else {
			fmt.Println("Published " + image)
		}
		time.Sleep(1 * time.Second)
	}
	client.Disconnect(0)
}
