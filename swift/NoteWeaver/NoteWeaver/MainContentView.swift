//
//  ContentView.swift
//  NoteWeaver
//
//  Created by Srikur Kanuparthy on 4/17/24.
//

import SwiftUI

struct MainContentView: View {
    @State private var selectedPage: Image? = nil
    @State private var images = ["image1", "image2"]
    
    var body: some View {
        NavigationView {
            List(images, id: \.self) { imageName in
                Text(imageName)
                    .onTapGesture {
                        // Here you would load the actual image
                        self.selectedPage = Image(imageName) // Assuming you have these images in your assets
                    }
            }
            .frame(minWidth: 200) // Adjust the width of the left pane
            
            if let image = selectedPage {
                image
                    .resizable()
                    .scaledToFit()
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                    .navigationTitle("NoteWeaver 0.0.1")
            } else {
                Text("Select an image from the left pane")
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
            
            VStack(alignment: .leading) {
                Text("Information and Controls")
                    .font(.headline)
                Divider()
                Text("Details about the selected music sheet will appear here.")
                Spacer()
                Button("Do Something") {
                    // Implement your button action here
                }
            }
            .frame(minWidth: 200) // Adjust the width of the right pane
        }
    }
}

#Preview {
    MainContentView()
}
