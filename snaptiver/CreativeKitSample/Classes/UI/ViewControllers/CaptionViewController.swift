//
//  CaptionViewController.swift
//  CreativeKitSample
//
//  Created by Samuel Chow on 3/27/19.
//  Copyright © 2019 Snap Inc. All rights reserved.
//

import UIKit
import SwiftSocket

class CaptionViewController: UIViewController {
  // This is for the UDPport
    let host = "188.166.115.7"
    let port = 7001
    
  // Visual components
    
var timer = Timer()
   
  
  @IBOutlet weak var textField: UITextField?
  
    @IBOutlet weak var spprice: UITextView!
    // MARK: - Event handlers
  
    @IBOutlet weak var esxprice: UITextView!
    
    @IBAction func cancelDidTap() {
    dismiss(animated: true)
  }
    
    var captionPrice = " ";
    var ticker = " ";
    var capspprice = " ";
    var capexpprice = " ";

    @IBAction func refreshButton(_ sender: Any) {
        reloadPrice()
    }
    
    @IBAction func spprepare(_ sender: Any) {
        ticker = "SP Futures"
    }
    
    @IBAction func esxprepare(_ sender: Any) {
        ticker = "ESX Futures"
    }
    
    @objc func textFieldDidChange(_ textField: UITextField) {
    if textField.text == String.empty {
      navigationItem.rightBarButtonItem?.title = "Skip"
    } else {
      navigationItem.rightBarButtonItem?.title = "Next"
    }
  }
  
  // MARK: - UIViewController
  
  override func viewDidLoad() {
    super.viewDidLoad()
//        reloadPrice()
    Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true, block: { timer in
        self.reloadPrice()
    })
    
    

//    textField?.addTarget(self, action: #selector(textFieldDidChange(_:)), for: .editingChanged)
  }
  
  override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
    if segue.identifier == "showStickers" {
      if let stickersController = segue.destination as? StickersViewController {
        stickersController.caption = "Current Price for " + ticker + " is: " + captionPrice
      }
    }
  }
    

    
    func reloadPrice(){
        let client = UDPClient(address: host, port: Int32(port))
        
        switch client.send(string: "TYPE=SUBSCRIPTION_REQUEST") {
        case .success:
            print("Connected")
        case .failure(let error):
            print("Client failed to send message to server: \(error)")
        }
        
        //    self.textField.text = "0000"
        
        
        let(byteArray, senderIPAddress, senderPort) = client.recv(1024)
        print("client's recv() returned")
        
        if let byteArray = byteArray,
            let string = String(data: Data(byteArray), encoding: .utf8)
        {
            //            print("Cient received: \(string)\nsender: \(senderIPAddress)\nport: \(senderPort)")
            var datastream = string.split(separator: "|").map(String.init)
            print(datastream[0])
            if datastream[0].contains("TRADE") {
                if  string.contains("SP") {
                    //Case SP-FUTURE
                    let spprice = datastream[3]
                    let spval = spprice.split(separator: "=").map(String.init)[1]
                    self.spprice?.text = "€" + spval
                    ticker = "SP-Future"
                    captionPrice = "€" + spval
                } else if string.contains("ESX") {
                    //Case ESX-FUTURE
                    let esxprice = datastream[3]
                    let esxval = esxprice.split(separator: "=").map(String.init)[1]
                    self.esxprice?.text = "€" + esxval
                    ticker = "ESX-Future"
                    captionPrice = "€" + esxval
                }
            }
//            print(display)
            
        }
        else {
            print("error in client while trying to recv()")
        }
    }
    
}

