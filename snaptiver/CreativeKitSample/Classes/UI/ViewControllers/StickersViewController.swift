//
//  StickersViewController.swift
//  CreativeKitSample
//
//  Created by Samuel Chow on 3/27/19.
//  Copyright © 2019 Snap Inc. All rights reserved.
//

import UIKit

import FLAnimatedImage
import SCSDKCreativeKit

class StickersViewController: UIViewController {
  // Configuration
  
  enum Constants {
    static let reuseIdentifier = "StickerGridCellIdentifer"
  }
  
  // Visual components
  
  @IBOutlet weak var collectionView: UICollectionView?
  @IBOutlet weak var shareButton: UIBarButtonItem?
  
  // State variables
  
  public var caption: String?
  private var selectedIndex: IndexPath?
  private let stickers = [
    Media(name: "applogo.png", source: .bundle, type: .still),
    Media(name: "applogosquare.png", source: .bundle, type: .still),
    Media(name: "snaptiverlogo.png", source: .bundle, type: .still),
  ]
    
    // Snapchat stuff
    
  
  // MARK: - Event Handlers
  
  @IBAction func shareDidTap() {
    guard let selectedIndex = selectedIndex else {
      print("Need to select a sticker")
      return
    }
    
    let selectedCell = collectionView?.cellForItem(at: selectedIndex) as? ImageCollectionViewCell
    var sticker:SCSDKSnapSticker? = nil
    if selectedCell?.media?.type == .still {
      guard let stickerImage = selectedCell?.animView?.image else {
        return
      }

      sticker = SCSDKSnapSticker(stickerImage: stickerImage)
    } else if selectedCell?.media?.type == .animated {
      if selectedCell?.media?.source == .remote {
        guard let urlString = selectedCell?.media?.name,
          let url = URL(string: urlString) else {
            return
        }

        sticker = SCSDKSnapSticker(stickerUrl: url, isAnimated: true)
      }
    }
    

    let snap = SCSDKNoSnapContent()
    snap.sticker = sticker;
    snap.caption = caption;
    snap.attachmentUrl = "https://www.optiver.com";
    
    
    // Send it over to Snapchat
    view.isUserInteractionEnabled = false
    snapAPI?.startSending(snap) { [weak self] (error: Error?) in
        self?.view.isUserInteractionEnabled = true
    }
//    snapAPI.startSnapping
  }
  
  @IBAction func cancelDidTap() {
    dismiss(animated: true)
  }
  
  // MARK: - UIViewController
    var snapAPI: SCSDKSnapAPI?
  
  override func viewDidLoad() {
    super.viewDidLoad()
    
    snapAPI = SCSDKSnapAPI()
  }
}

extension StickersViewController: UICollectionViewDataSource {
  func numberOfSectionsInCollectionView(collectionView: UICollectionView) -> Int {
    return 1
  }
  
  func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
    return stickers.count
  }
  
  func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
    let cell = collectionView.dequeueReusableCell(withReuseIdentifier: Constants.reuseIdentifier,
                                                  for: indexPath)
    guard let imageCell = cell as? ImageCollectionViewCell else {
      return cell
    }
    
    imageCell.media = stickers[indexPath.row]
    
    return imageCell
  }
}

extension StickersViewController: UICollectionViewDelegate {
  func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
    if let selectedIndex = selectedIndex {
      guard let prevSelectedCell = collectionView.cellForItem(at: selectedIndex)
        as? ImageCollectionViewCell else {
          return
      }

      prevSelectedCell.select(withColor: UIColor.clear)
    }
    
    guard let selectedCell = collectionView.cellForItem(at: indexPath) as?
      ImageCollectionViewCell else {
        return
    }
    
    selectedCell.select(withColor: UIColor.orange)
    selectedIndex = indexPath
    shareButton?.isEnabled = true
  }
}

