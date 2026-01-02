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

// Socket events
export interface ServerToClientEvents {
    //  defines functions that the server can call on the client
    room_update: (data: GameState) => void;
    deal_hand: (data: { hand: Card[] }) => void;
    error: (data: { message: string }) => void;
}

export interface ClientToServerEvents {
    // defines functions that the client can call on the server
    join_game: (data: { room: string; name: string }) => void;
    start_game: (data: { room: string }) => void;
}