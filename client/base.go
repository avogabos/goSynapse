package client

import "net/http"

type SynapseClient struct {
	Host        string
	Port        string
	ApiKey      string
	HttpClient  *http.Client
	BaseRequest *http.Request
	AuthCookie  string
}

func NewSynapseClient(host string, port string, apiKey string) *SynapseClient {
	client := &http.Client{}
	baseReq := &http.Request{}
	baseReq.Header = make(http.Header)
	if apiKey != "" {
		baseReq.Header.Add(apiKeyHeader, apiKey)
	}
	return &SynapseClient{
		Host:        host,
		Port:        port,
		HttpClient:  client,
		ApiKey:      apiKey,
		BaseRequest: baseReq,
	}
}
