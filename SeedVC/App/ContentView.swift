
import SwiftUI
import AVFoundation
import CoreML

struct ContentView: View {
    @StateObject private var audioManager = AudioManager.shared
    @StateObject private var audioRecorder = AudioRecorder()
    @State private var sourceAudioURL: URL?
    @State private var targetAudioURL: URL?
    @State private var progress: Double = 0.0
    @State private var isConverting: Bool = false
    @State private var outputAudioURL: URL?
    
    init() {
        _ = AVAudioSession.sharedInstance()
        try? AVAudioSession.sharedInstance().setCategory(.playAndRecord, mode: .default, options: [.allowBluetooth, .allowAirPlay])
        try? AVAudioSession.sharedInstance().setActive(true)
    }
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Header
                Text("Seed-VC Voice Converter")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                
                Spacer()
                
                // Source Audio Selection
                VStack(alignment: .leading, spacing: 10) {
                    Text("Source Audio:")
                        .font(.headline)
                    
                    Button(action: pickSourceAudio) {
                        HStack {
                            Image(systemName: "music.note")
                            Text(sourceAudioURL.map { "File: \($0.lastPathComponent)" } ?? "Choose Source")
                            Spacer()
                            Image(systemName: "chevron.right")
                        }
                    }
                }
                
                // Target Audio Selection
                VStack(alignment: .leading, spacing: 10) {
                    Text("Target Voice:")
                        .font(.headline)
                    
                    Button(action: pickTargetAudio) {
                        HStack {
                            Image(systemName: "person.fill")
                            Text(targetAudioURL.map { "File: \($0.lastPathComponent)" } ?? "Choose Target")
                            Spacer()
                            Image(systemName: "chevron.right")
                        }
                    }
                }
                
                // Convert Button
                Button(action: convertVoice) {
                    if isConverting {
                        ProgressView()
                            .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    } else {
                        Text("Convert Voice")
                            .font(.title2)
                            .fontWeight(.semibold)
                    }
                }
                .disabled(!audioManager.isModelLoaded || sourceAudioURL == nil || targetAudioURL == nil || isConverting)
                .padding()
                .background(isConverting ? Color.gray : Color.blue)
                .foregroundColor(.white)
                .cornerRadius(10)
                
                // Progress
                if isConverting {
                    VStack(spacing: 10) {
                        Text("Converting...")
                            .font(.headline)
                        LinearProgressView(progress: progress, target: 1.0)
                    }
                }
                
                // Output
                if let outputURL = outputAudioURL {
                    VStack(alignment: .leading, spacing: 10) {
                        Text("Result:")
                            .font(.headline)
                        
                        Button(action: playOutput) {
                            HStack {
                                Image(systemName: "play.circle.fill")
                                Text(outputURL.lastPathComponent)
                            }
                        }
                    }
                }
                
                Spacer()
            }
            .padding()
        }
        .navigationTitle("Seed-VC")
        .onAppear {
            audioManager.loadModels()
        }
    }
    
    private func pickSourceAudio() {
        let picker = UIDocumentPickerViewController(forOpeningContentTypes: [.audio], asCopy: true)
        picker.delegate = self
    }
    
    private func pickTargetAudio() {
        let picker = UIDocumentPickerViewController(forOpeningContentTypes: [.audio], asCopy: true)
        picker.delegate = self
    }
    
    private func convertVoice() {
        isConverting = true
        progress = 0.0
        
        // Convert voice using CoreML models
        Task {
            await audioManager.convert(sourceAudioURL!, targetAudioURL!) { result in
                self.isConverting = false
                self.progress = 1.0
                self.outputAudioURL = result
            }
        }
    }
    
    private func playOutput() {
        // Play the output audio
        let player = AVAudioPlayer?(outputAudioURL!)
    }
}

// LinearProgressView for smooth progress animation
struct LinearProgressView: View {
    let progress: Double
    let target: Double
    
    var body: some View {
        GeometryReader { geometry in
            ZStack(alignment: .leading) {
                Rectangle()
                    .fill(Color.gray.opacity(0.3))
                    .frame(height: 10)
                
                Rectangle()
                    .fill(Color.green)
                    .frame(width: (progress / target) * geometry.size.width, height: 10)
            }
        }
    }
}

// DocumentPickerDelegate extension
extension ContentView: UIDocumentPickerDelegate {
    func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
        if let url = urls.first {
            if controller == sourceAudioPicker {
                sourceAudioURL = url
            } else if controller == targetAudioPicker {
                targetAudioURL = url
            }
        }
    }
}
