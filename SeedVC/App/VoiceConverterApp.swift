
import SwiftUI

@main
struct VoiceConverterApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(AudioManager.shared)
        }
    }
}

// AudioManager for CoreML model management
class AudioManager: ObservableObject {
    static let shared = AudioManager()
    
    @Published var isModelLoaded: Bool = false
    @Published var errorMessage: String?
    
    func loadModels() {
        // Load CoreML models here
        isModelLoaded = true
    }
}
