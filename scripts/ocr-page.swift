import Foundation
import Vision
import ImageIO

guard CommandLine.arguments.count == 2 else {
    fputs("usage: ocr-page image\n", stderr)
    exit(2)
}

let imageURL = URL(fileURLWithPath: CommandLine.arguments[1])
guard let source = CGImageSourceCreateWithURL(imageURL as CFURL, nil),
      let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
    fputs("could not read image\n", stderr)
    exit(1)
}

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = true
request.recognitionLanguages = ["en-US"]

do {
    try VNImageRequestHandler(cgImage: image).perform([request])
    let observations = request.results ?? []
    let lines = observations.compactMap { $0.topCandidates(1).first?.string }
    print(lines.joined(separator: "\n"))
} catch {
    fputs("ocr failed: \(error)\n", stderr)
    exit(1)
}
