
import CoreML
import Foundation

class ModelLoader {
    static let shared = ModelLoader()
    
    func loadWhisperModel() -> WhisperFeatureExtractor? {
        // Load Whisper model from CoreMLModels/WhisperFeatureExtractor.mlmodel
        guard let modelURL = Bundle.main.url(forResource: "WhisperFeatureExtractor", withExtension: "mlmodel") else {
            print("Whisper model not found")
            return nil
        }
        
        do {
            return try WHISPERFeatureExtractor(configuration: .default).loadModel(modelURL)
        } catch {
            print("Error loading Whisper model: \(error)")
            return nil
        }
    }
    
    func loadDiTModel() -> DiTVoiceConverter? {
        // Load DiT model from CoreMLModels/DiTVoiceConverter.mlmodel
        guard let modelURL = Bundle.main.url(forResource: "DiTVoiceConverter", withExtension: "mlmodel") else {
            print("DiT model not found")
            return nil
        }
        
        do {
            return try DiTVoiceConverter(configuration: .default).loadModel(modelURL)
        } catch {
            print("Error loading DiT model: \(error)")
            return nil
        }
    }
    
    func loadVocoderModel() -> BigVGANVocoder? {
        // Load Vocoder model from CoreMLModels/BigVGANVocoder.mlmodel
        guard let modelURL = Bundle.main.url(forResource: "BigVGANVocoder", withExtension: "mlmodel") else {
            print("Vocoder model not found")
            return nil
        }
        
        do {
            return try BigVGANVocoder(configuration: .default).loadModel(modelURL)
        } catch {
            print("Error loading Vocoder model: \(error)")
            return nil
        }
    }
}
