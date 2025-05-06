package client

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
)

// Struct definitions remain the same
type InitData struct {
	Tick    int64  `json:"tick"`
	Text    string `json:"text"`
	Abstick int64  `json:"abstick"`
	Hash    string `json:"hash"`
	Task    string `json:"task"`
}

type NodeData struct {
	Iden     string            `json:"iden"`
	Tags     map[string]string `json:"tags"`
	Props    NodeProps         `json:"props"`
	TagProps map[string]string `json:"tagprops"`
	NodeData map[string]string `json:"nodedata"`
	Path     map[string]string `json:"path"`
}

type NodeProps struct {
	Created int64   `json:".created"`
	Name    string  `json:"name "`
	Seen    []int64 `json:".seen"`
	Type    string  `json:"type"`
	Desc    string  `json:"desc"`
	Leaker  string  `json:"leaker"`
}

type Node struct {
	Key  string     `json:"key"`
	Data [][]string `json:"data"`
	Info NodeData   `json:"info"`
}

type FiniData struct {
	Tock    int64 `json:"tock"`
	Abstock int64 `json:"abstock"`
	Took    int   `json:"took"`
	Count   int   `json:"count"`
}

// ParseJSONStream handles multiple JSON arrays in a stream
func ParseJSONStream(input []byte) ([]InitData, []Node, []FiniData, error) {
	reader := bufio.NewReader(bytes.NewReader(input))

	var initList []InitData
	var nodeList []Node
	var finiList []FiniData

	decoder := json.NewDecoder(reader)

	// Read JSON elements in sequence
	for {
		var data []interface{}
		if err := decoder.Decode(&data); err == io.EOF {
			break
		} else if err != nil {
			return nil, nil, nil, fmt.Errorf("error parsing JSON: %w", err)
		}

		// Process each JSON entry
		switch data[0].(string) {
		case "init":
			var init InitData
			bytes, _ := json.Marshal(data[1])
			json.Unmarshal(bytes, &init)
			initList = append(initList, init)

		case "node":
			node := Node{Key: "node"}
			if nodeArray, ok := data[1].([]interface{}); ok {
				// Extract node pairs
				if nodePairs, ok := nodeArray[0].([]interface{}); ok {
					for _, pair := range nodePairs {
						if pairSlice, ok := pair.([]interface{}); ok {
							var strPair []string
							for _, item := range pairSlice {
								if str, ok := item.(string); ok {
									strPair = append(strPair, str)
								}
							}
							node.Data = append(node.Data, strPair)
						}
					}
				}

				// Extract node properties
				bytes, _ := json.Marshal(nodeArray[1])
				json.Unmarshal(bytes, &node.Info)
			}
			nodeList = append(nodeList, node)

		case "fini":
			var fini FiniData
			bytes, _ := json.Marshal(data[1])
			json.Unmarshal(bytes, &fini)
			finiList = append(finiList, fini)
		}
	}

	return initList, nodeList, finiList, nil
}
