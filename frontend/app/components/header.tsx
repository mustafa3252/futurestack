interface HeaderProps {
  setUserEmail: (email: string) => void;
}

export default function Header({ setUserEmail }: HeaderProps) {
  return (
    <div className="flex justify-between items-center">
      <div className="flex items-center gap-4">
        <div className="text-5xl">🔍</div>
        <div>
          <h1 className="text-4xl font-bold text-white bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            StartupScout
          </h1>
          <p className="text-cyan-400 text-sm font-light mt-1">
            Powered by Cerebras Llama 4 • 2000+ tokens/sec
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <div className="relative group">
          <input
            type="email"
            placeholder="Enter your email"
            className="px-4 py-2 rounded bg-gray-700 text-white w-64"
            onChange={(e) => setUserEmail(e.target.value)}
          />
          <div className="absolute hidden group-hover:block right-0 top-full mt-2 p-2 bg-gray-800 text-white text-sm rounded-lg w-64">
            Leave your email and you will be sent the artifacts when done
          </div>
        </div>
      </div>
    </div>
  );
}
