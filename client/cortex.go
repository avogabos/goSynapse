package client

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/url"
)

const (
	feed        = "/api/v1/feed"
	storm       = "/api/v1/storm"
	stormCall   = "/api/v1/storm/call"
	stormNodes  = "/api/v1/storm/nodes"
	stormExport = "/api/v1/storm/export"
	model       = "/api/v1/model"
	modelNorm   = "/api/v1/model/norm"
	varsGet     = "/api/v1/vars/get"
	varsSet     = "/api/v1/vars/set"
	varsPop     = "/api/v1/vars/pop"
	coreInfo    = "/api/v1/core/info"
)

func (s *SynapseClient) Feed(nodes Nodes) error {
	newReq := s.BaseRequest
	newReq.Method = "POST"
	reqUrl := s.Host + ":" + s.Port + feed
	err := error(nil)
	newReq.URL, err = url.Parse(reqUrl)
	if err != nil {
		return err
	}

	jsonBody, err := json.Marshal(nodes)
	if err != nil {
		return err
	}

	bodyBuffer := bytes.NewBuffer(jsonBody)
	newReq.Body = io.NopCloser(bodyBuffer)

	resp, err := s.HttpClient.Do(newReq)
	if err != nil {
		return err
	}

	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	respJson := GenericMessage{}
	err = json.Unmarshal(bodyBytes, &respJson)
	if err != nil {
		return err
	}
	if respJson.Status != "ok" {
		respError := ErrorMessage{}
		err = json.Unmarshal(bodyBytes, &respError)
		if err != nil {
			return errors.New("Feed failed: " + err.Error())
		}
	}
	return nil
}

func (s *SynapseClient) Storm(stormQuery string, opts []string, stream string) ([]Node, error) {
	newReq := s.BaseRequest
	newReq.Method = "GET"
	reqUrl := "https://" + s.Host + ":" + s.Port + storm
	err := error(nil)
	newReq.URL, err = url.Parse(reqUrl)
	if err != nil {
		return nil, err
	}

	stormQ := Storm{
		Query:  stormQuery,
		Opts:   opts,
		Stream: stream,
	}

	jsonBody, err := json.Marshal(stormQ)
	if err != nil {
		return nil, err
	}

	bodyBuffer := bytes.NewBuffer(jsonBody)
	newReq.Body = io.NopCloser(bodyBuffer)

	resp, err := s.HttpClient.Do(newReq)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	init, nodes, fini, err := ParseJSONStream(bodyBytes)

	if err != nil {
		return nil, err
	}
	fmt.Println(init)
	fmt.Println(nodes)
	fmt.Println(fini)

	return nodes, nil
}

func (s *SynapseClient) StormCall(stormQuery string, opts []string) (string, error) {
	newReq := s.BaseRequest
	newReq.Method = "GET"
	reqUrl := s.Host + ":" + s.Port + stormCall
	err := error(nil)
	newReq.URL, err = url.Parse(reqUrl)
	if err != nil {
		return "", err
	}

	stormCall := StormCall{
		Query: stormQuery,
		Opts:  opts,
	}

	jsonBody, err := json.Marshal(stormCall)
	if err != nil {
		return "", err
	}

	bodyBuffer := bytes.NewBuffer(jsonBody)
	newReq.Body = io.NopCloser(bodyBuffer)

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
			return "", errors.New("StormCall failed: " + err.Error())
		}
	}

	return string(bodyBytes), nil
}

func (s *SynapseClient) StormExport(stormQuery string, opts []string) (string, error) {
	newReq := s.BaseRequest
	newReq.Method = "GET"
	reqUrl := s.Host + ":" + s.Port + stormExport
	err := error(nil)
	newReq.URL, err = url.Parse(reqUrl)
	if err != nil {
		return "", err
	}

	stormCall := StormCall{
		Query: stormQuery,
		Opts:  opts,
	}

	jsonBody, err := json.Marshal(stormCall)
	if err != nil {
		return "", err
	}

	bodyBuffer := bytes.NewBuffer(jsonBody)
	newReq.Body = io.NopCloser(bodyBuffer)

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
			return "", errors.New("StormExport failed: " + err.Error())
		}
	}

	return string(bodyBytes), nil
}

func (s *SynapseClient) Model() (CortexModel, error) {
	newReq := s.BaseRequest
	newReq.Method = "GET"
	reqUrl := s.Host + ":" + s.Port + model
	err := error(nil)
	newReq.URL, err = url.Parse(reqUrl)
	if err != nil {
		return CortexModel{}, err
	}

	resp, err := s.HttpClient.Do(newReq)
	if err != nil {
		return CortexModel{}, err
	}

	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return CortexModel{}, err
	}

	respJson := CortexModel{}
	err = json.Unmarshal(bodyBytes, &respJson)
	if err != nil {
		respError := ErrorMessage{}
		err = json.Unmarshal(bodyBytes, &respError)
		if err != nil {
			return CortexModel{}, errors.New("Model failed: " + err.Error())
		}
		return respJson, errors.New("Model failed: " + respError.Mesg)
	}

	return respJson, nil
}
