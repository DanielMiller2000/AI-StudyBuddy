import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { ChevronLeft, ChevronRight, BookOpen, Flag, Check } from 'lucide-react';

const FlashCardGenerator = () => {
  // State for card management
  const [cards, setCards] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [inputText, setInputText] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [studyStats, setStudyStats] = useState({
    mastered: 0,
    learning: 0,
    flagged: 0
  });

  // Mock function to simulate API call to our backend models
  const generateFlashCards = async (text) => {
    setIsGenerating(true);
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Mock response - in real implementation, this would call our backend models
    const mockCards = [
      {
        front: "What is Natural Language Processing?",
        back: "NLP is a field of AI that focuses on the interaction between computers and human language. It involves processing and analyzing large amounts of natural language data.",
        keywords: ["NLP", "AI", "language processing"],
        summary: "NLP enables computers to understand and process human language.",
        status: 'learning'
      },
      {
        front: "Explain BERT's architecture",
        back: "BERT is a transformer-based model that uses bidirectional training of text. It learns context from both left and right sides of each word.",
        keywords: ["BERT", "transformer", "bidirectional"],
        summary: "BERT uses bidirectional context to understand text.",
        status: 'learning'
      }
    ];

    setCards(mockCards);
    setIsGenerating(false);
    setCurrentIndex(0);
  };

  // Navigation functions
  const nextCard = () => {
    if (currentIndex < cards.length - 1) {
      setCurrentIndex(prev => prev + 1);
      setIsFlipped(false);
    }
  };

  const prevCard = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
      setIsFlipped(false);
    }
  };

  // Card status management
  const updateCardStatus = (status) => {
    const updatedCards = [...cards];
    updatedCards[currentIndex].status = status;
    setCards(updatedCards);

    // Update study statistics
    const newStats = {
      mastered: updatedCards.filter(card => card.status === 'mastered').length,
      learning: updatedCards.filter(card => card.status === 'learning').length,
      flagged: updatedCards.filter(card => card.status === 'flagged').length
    };
    setStudyStats(newStats);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* Input Section */}
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Generate Flash Cards</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <Textarea 
              placeholder="Enter your study text here..." 
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="h-32"
            />
            <Button 
              onClick={() => generateFlashCards(inputText)}
              disabled={!inputText || isGenerating}
              className="w-full"
            >
              {isGenerating ? "Generating..." : "Generate Flash Cards"}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Flash Card Display */}
      {cards.length > 0 && (
        <div className="space-y-6">
          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentIndex + 1) / cards.length) * 100}%` }}
            />
          </div>

          {/* Study Statistics */}
          <div className="grid grid-cols-3 gap-4">
            <Card className="bg-green-50">
              <CardContent className="p-4 text-center">
                <Check className="w-6 h-6 mx-auto mb-2 text-green-600" />
                <div className="text-lg font-bold text-green-600">{studyStats.mastered}</div>
                <div className="text-sm text-green-600">Mastered</div>
              </CardContent>
            </Card>
            <Card className="bg-blue-50">
              <CardContent className="p-4 text-center">
                <BookOpen className="w-6 h-6 mx-auto mb-2 text-blue-600" />
                <div className="text-lg font-bold text-blue-600">{studyStats.learning}</div>
                <div className="text-sm text-blue-600">Learning</div>
              </CardContent>
            </Card>
            <Card className="bg-yellow-50">
              <CardContent className="p-4 text-center">
                <Flag className="w-6 h-6 mx-auto mb-2 text-yellow-600" />
                <div className="text-lg font-bold text-yellow-600">{studyStats.flagged}</div>
                <div className="text-sm text-yellow-600">Flagged</div>
              </CardContent>
            </Card>
          </div>

          {/* Flash Card */}
          <Card 
            className="w-full h-64 cursor-pointer relative"
            onClick={() => setIsFlipped(!isFlipped)}
          >
            <CardContent className="h-full p-6">
              <div className={`absolute inset-0 w-full h-full transition-opacity duration-300 ${
                isFlipped ? 'opacity-0' : 'opacity-100'
              }`}>
                <div className="p-6">
                  <div className="text-xl font-semibold mb-4">
                    {cards[currentIndex].front}
                  </div>
                  <div className="text-sm text-gray-500">
                    Click to reveal answer
                  </div>
                </div>
              </div>
              <div className={`absolute inset-0 w-full h-full transition-opacity duration-300 ${
                isFlipped ? 'opacity-100' : 'opacity-0'
              }`}>
                <div className="p-6">
                  <div className="text-lg mb-4">
                    {cards[currentIndex].back}
                  </div>
                  <div className="text-sm text-gray-600">
                    <div className="mb-2">
                      <span className="font-semibold">Key Concepts: </span>
                      {cards[currentIndex].keywords.join(", ")}
                    </div>
                    <div>
                      <span className="font-semibold">Summary: </span>
                      {cards[currentIndex].summary}
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Navigation Controls */}
          <div className="flex justify-between items-center">
            <Button
              variant="outline"
              onClick={prevCard}
              disabled={currentIndex === 0}
            >
              <ChevronLeft className="w-4 h-4 mr-2" />
              Previous
            </Button>
            
            <div className="space-x-2">
              <Button
                variant="outline"
                onClick={() => updateCardStatus('flagged')}
                className="text-yellow-600"
              >
                <Flag className="w-4 h-4" />
              </Button>
              <Button
                variant="outline"
                onClick={() => updateCardStatus('learning')}
                className="text-blue-600"
              >
                <BookOpen className="w-4 h-4" />
              </Button>
              <Button
                variant="outline"
                onClick={() => updateCardStatus('mastered')}
                className="text-green-600"
              >
                <Check className="w-4 h-4" />
              </Button>
            </div>

            <Button
              variant="outline"
              onClick={nextCard}
              disabled={currentIndex === cards.length - 1}
            >
              Next
              <ChevronRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default FlashCardGenerator;