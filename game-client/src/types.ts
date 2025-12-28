export type Suit = 'Spades' | 'Hearts' | 'Diamonds' | 'Clubs';

export interface Card {
    suit: Suit;
    rank: string;
}

export interface Player {
    uid: number;
    name: string;
    hand: Card[];
}

export interface GameState {
    player_count: number;
    players: Player[];
    started: boolean;
    current_turn: string | null;
}

// These interfaces define the "Contract" for our Socket events
export interface ServerToClientEvents {
    room_update: (data: GameState) => void;
    deal_hand: (data: { hand: Card[] }) => void;
    error: (data: { message: string }) => void;
}

export interface ClientToServerEvents {
    join_game: (data: { room: string; name: string }) => void;
    start_game: (data: { room: string }) => void;
}