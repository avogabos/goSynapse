package client

import (
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"net/url"
)

const (
	axonDel = "/api/v1/axon/files/del"
	axonPut = "/api/v1/axon/files/put"
	axonHas = "/api/v1/axon/files/has/sha256/"
	axonGet = "/api/v1/axon/files/by/sha256/"
)

func (s *SynapseClient) AxonDelete(sha256s []string) (AxonDelete, error) {
	deleteShas := map[string][]string{
		"sha256": sha256s,
	}

	newReq := s.BaseRequest
	newReq.Method = "POST"
	reqUrl := s.Host + ":" + s.Port + axonDel
	err := error(nil)
	newReq.URL, err = url.Parse(reqUrl)
	if err != nil {
		return AxonDelete{}, err
	}

	reqBytes, err := json.Marshal(deleteShas)
	if err != nil {
		return AxonDelete{}, err
	}

	newReq.Body = io.NopCloser(bytes.NewBuffer(reqBytes))

	resp, err := s.HttpClient.Do(newReq)
	if err != nil {
		return AxonDelete{}, err
	}

	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return AxonDelete{}, err
	}

	respJson := AxonDelete{}
	err = json.Unmarshal(bodyBytes, &respJson)
	if err != nil {
		return AxonDelete{}, err
	}
	if respJson.Status != "ok" {
		respError := ErrorMessage{}
		err = json.Unmarshal(bodyBytes, &respError)
		if err != nil {
			return AxonDelete{}, errors.New("AxonDelete failed: " + err.Error())
		}
	}
	return respJson, nil
}

func (s *SynapseClient) AxonPut(fileBytes []byte) (string, error) {
	newReq := s.BaseRequest
	newReq.Method = "POST"
	reqUrl := s.Host + ":" + s.Port + axonPut
	err := error(nil)
	newReq.URL, err = url.Parse(reqUrl)
	if err != nil {
		return "", err
	}

	newReq.Body = io.NopCloser(bytes.NewBuffer(fileBytes))

	resp, err := s.HttpClient.Do(newReq)
	if err != nil {
		return "", err
	}

	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	respJson := GenericMessage{}
	err = json.Unmarshal(bodyBytes, &respJson)
	if err != nil {
		return "", err
	}
	if respJson.Status != "ok" {
		respError := ErrorMessage{}
		err = json.Unmarshal(bodyBytes, &respError)
		if err != nil {
			return "", errors.New("AxonPut failed: " + err.Error())
		}
	}
	return string(bodyBytes), nil
}

func (s *SynapseClient) AxonHas(sha256 string) (bool, error) {
	newReq := s.BaseRequest
	newReq.Method = "GET"
	reqUrl := s.Host + ":" + s.Port + axonHas + sha256
	err := error(nil)
	newReq.URL, err = url.Parse(reqUrl)
	if err != nil {
		return false, err
	}

	resp, err := s.HttpClient.Do(newReq)
	if err != nil {
		return false, err
	}

	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return false, err
	}

	respJson := GenericMessage{}
	err = json.Unmarshal(bodyBytes, &respJson)
	if err != nil {
		return false, err
	}
	if respJson.Status != "ok" {
		respError := ErrorMessage{}
		err = json.Unmarshal(bodyBytes, &respError)
		if err != nil {
			return false, errors.New("AxonHas failed: " + err.Error())
		}
	}
	return true, nil
}

func (s *SynapseClient) AxonGet(sha256 string) (io.Reader, error) {
	newReq := s.BaseRequest
	newReq.Method = "GET"
	reqUrl := s.Host + ":" + s.Port + axonGet + sha256
	err := error(nil)
	newReq.URL, err = url.Parse(reqUrl)
	if err != nil {
		return nil, err
	}

	resp, err := s.HttpClient.Do(newReq)
	if err != nil {
		return nil, err
	}

	return resp.Body, nil
}
